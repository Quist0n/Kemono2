import time

from typing import List

from flask import Request

from src.internals.database.database import get_cursor
from src.internals.cache.redis import (
    get_conn,
    KemonoRedisLock,
    serialize_dict_list,
    deserialize_dict_list
)

from src.utils.utils import paysite_list

from .types import (
    Artist,
    PaginationDB,
    PaginationInit,
    TDArtistListParams,
    ValidationResult
)


def validate_artists_request(requestArg: Request):
    """
    Validate parameters for artist search from request
    """
    search_params: TDArtistListParams = requestArg.args.to_dict()
    # Validattions:
    # - `name`
    # - `service`
    #     - if absent, search all services, otherwise only one
    #     - is a string
    #     - is a valid service name
    pagination_init = PaginationInit(**search_params)
    result_data = dict(
        pagination_init=pagination_init
    )

    service = search_params.get("service")
    errors = None
    is_valid = False

    if service not in paysite_list and service is not None:

        errors = [dict(message=f"Invalid service parameter. Service must be one of {paysite_list}")]

    if not errors:
        is_valid = True

    if is_valid is True:
        return ValidationResult(
            is_successful=True,
            data=result_data,
            validation_errors=errors
        )

    else:
        return ValidationResult(
            is_successful=False,
            data=result_data,
            validation_errors=errors
        )


def count_artists(service: str = None) -> int:
    """"""
    cursor = get_cursor()
    arg_dict = dict(
        service=service
    )
    query = f"""
        SELECT COUNT(*) as artist_count
        FROM lookup
        WHERE
            service != 'discord-channel'
            {f"AND service = %(service)s" if service else ""}
    """
    cursor.execute(query, arg_dict)
    artist_count: int = cursor.fetchone()['artist_count']
    return artist_count


def get_artists_by_name(pagination_init: PaginationInit, name: str = None, service: str = None, reload: bool = False) -> List[Artist]:

    redis = get_conn()

    if name and service:
        key = f"artists_by_service_and_name:{service}:{name}"
    elif name and not service:
        key = f"artists_by_name:{name}"
    else:
        return get_artists(pagination_init, service=service, reload=reload)

    artists = redis.get(key)

    if artists and not reload:
        return deserialize_dict_list(artists)

    lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return get_artists_by_name(pagination_init, service=service, reload=reload)

    cursor = get_cursor()
    artist_count = count_artists(service)
    pagination_db = PaginationDB(pagination_init, artist_count)
    arg_dict = dict(
        service=service,
        name=name,
        **pagination_db.get_info()
    )

    query = f"""
        SELECT id, indexed, name, service, updated
        FROM lookup
        WHERE
            service != 'discord-channel'
            {f"AND service = %(service)s" if service else ""}
            {f"AND name = %(name)s" if name else ""}
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    cursor.execute(query, arg_dict)
    artists: List[Artist] = cursor.fetchall()
    redis.set(key, serialize_dict_list(artists), ex=600)
    return artists


def get_artists(pagination_init: PaginationInit, service: str = None, reload: bool = False) -> List[Artist]:
    """
    Get all artist information
    or
    optionally all artist information by service
    """
    redis = get_conn()

    if service:
        key = f"artists_by_service:{service}"
    else:
        key = "artist_all"

    artists = redis.get(key)

    if artists and not reload:
        return deserialize_dict_list(artists)

    lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return get_artists(pagination_init, service=service, reload=reload)

    cursor = get_cursor()
    artist_count = count_artists(service)
    pagination_db = PaginationDB(pagination_init, artist_count)
    arg_dict = dict(
        service=service,
        **pagination_db.get_info()
    )

    query = f"""
        SELECT id, indexed, name, service, updated
        FROM lookup
        WHERE
            service != 'discord-channel'
            {f"AND service = %(service)s" if service else ""}
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    cursor.execute(query, arg_dict)
    artists: List[Artist] = cursor.fetchall()
    redis.set(key, serialize_dict_list(artists), ex=600)
    return artists
