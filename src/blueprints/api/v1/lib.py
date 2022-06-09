import time
from typing import List, Union

from flask import Request

from src.internals.cache.redis import (
    KemonoRedisLock,
    create_counts_key_constructor,
    create_key_constructor,
    deserialize_dict_list,
    get_conn,
    serialize_dict_list
)
from src.internals.database.database import get_cursor
from src.utils.utils import paysite_list, encode_text_query

from .types import (
    TDArtist,
    TDArtistsParams,
    TDPaginationDB,
    TDValidationFailure,
    TDValidationSuccess
)

construct_artists_key = create_key_constructor("artists")
construct_artists_count_key = create_counts_key_constructor("artists")


def validate_artists_request(req: Request) -> Union[TDValidationFailure, TDValidationSuccess]:
    errors = []
    args_dict = req.args.to_dict()
    service = args_dict.get("service", "").strip()
    # name = args_dict.get("name", "").strip()

    if (service and service not in paysite_list):
        errors.append("Not a valid service")

    if (errors):
        result = TDValidationFailure(
            is_successful=False,
            errors=errors
        )

        return result

    validated_params = TDArtistsParams(
        service=service,
        # name=name
    )
    result = TDValidationSuccess(
        is_successful=True,
        data=validated_params
    )

    return result


def count_artists(
    service: str = None,
    # name: str = None,
    reload: bool = False
) -> int:
    redis = get_conn()
    # encoded_name = encode_text_query(name)
    redis_key = construct_artists_count_key(
        *("service", service) if service else "",
        # *("name", encoded_name) if name else ""
    )
    artist_count = redis.get(redis_key)
    result = None

    if artist_count and not reload:
        result = int(artist_count)
        return result

    lock = KemonoRedisLock(redis, redis_key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return count_artists(
            service,
            # name,
            reload=reload
        )

    cursor = get_cursor()
    query_args = dict(
        service=service,
        # name=name
    )

    # name_query = f"AND to_tsvector('english', name) @@ websearch_to_tsquery(%(name)s)" if name else ""

    query = f"""
        SELECT COUNT(*) as artist_count
        FROM lookup
        WHERE
            service != 'discord-channel'
            {"AND service = %(service)s" if service else ""}
    """
    cursor.execute(query, query_args)
    result = cursor.fetchone()
    artist_count: int = result['artist_count']
    redis.set(redis_key, str(artist_count), ex=600)
    lock.release()

    return artist_count


def get_artists(
    pagination_db: TDPaginationDB,
    service: str = None,
    # name: str = None,
    reload: bool = False
) -> List[TDArtist]:
    """
    Get all artist information.
    @TODO return dataclass
    """
    redis = get_conn()
    # encoded_name = encode_text_query(name)
    redis_key = construct_artists_key(
        *("service", service) if service else "",
        # *("name", encoded_name) if name else "",
        str(pagination_db["pagination_init"]["current_page"])
    )

    artists = redis.get(redis_key)

    if artists and not reload:
        return deserialize_dict_list(artists)

    lock = KemonoRedisLock(redis, redis_key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return get_artists(
            pagination_db,
            service,
            # name,
            reload=reload
        )

    cursor = get_cursor()
    arg_dict = dict(
        offset=pagination_db["offset"],
        limit=pagination_db["sql_limit"],
        service=service,
        # name=name
    )
    # name_query = f"AND to_tsvector('english', name) @@ websearch_to_tsquery(%(name)s)" if name else ""

    query = f"""
        SELECT id, indexed, name, service, updated
        FROM lookup
        WHERE
            service != 'discord-channel'
            {
                "AND service = %(service)s"
                if service
                else ""
            }
        ORDER BY
            indexed ASC,
            name ASC,
            service ASC
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    cursor.execute(query, arg_dict)
    artists: List[TDArtist] = cursor.fetchall()
    redis.set(redis_key, serialize_dict_list(artists), ex=600)
    lock.release()

    return artists
