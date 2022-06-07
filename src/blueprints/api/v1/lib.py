import time
from typing import List

from src.internals.cache.redis import (
    KemonoRedisLock,
    deserialize_dict_list,
    get_conn,
    serialize_dict_list
)
from src.internals.database.database import get_cursor
from src.utils.utils import paysite_list

from .types import TDArtist


def count_artists(reload: bool = False) -> int:
    redis = get_conn()
    redis_key = "counts:artists"
    artist_count = redis.get(redis_key)
    result = None

    if artist_count and not reload:
        result = int(artist_count)
        return result

    lock = KemonoRedisLock(redis, redis_key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return count_artists(reload=reload)

    cursor = get_cursor()
    query = """
        SELECT COUNT(*) as artist_count
        FROM lookup
        WHERE
            service != 'discord-channel'
    """
    cursor.execute(query)
    result = cursor.fetchone()
    artist_count: int = result['artist_count']
    redis.set(redis_key, str(artist_count), ex=600)
    lock.release()

    return artist_count


def get_artists(
    current_page: int,
    offset: int,
    limit: int,
    reload: bool = False
) -> List[TDArtist]:
    """
    Get all artist information.
    @TODO return dataclass
    """
    redis = get_conn()
    redis_key = f"artists:{str(current_page)}"

    artists = redis.get(redis_key)

    if artists and not reload:
        return deserialize_dict_list(artists)

    lock = KemonoRedisLock(redis, redis_key, expire=60, auto_renewal=True)

    if not lock.acquire(blocking=False):
        time.sleep(0.1)
        return get_artists(current_page, offset, limit, reload=reload)

    cursor = get_cursor()
    arg_dict = dict(
        offset=offset,
        limit=limit
    )
    query = """
        SELECT id, indexed, name, service, updated
        FROM lookup
        WHERE
            service != 'discord-channel'
        ORDER BY
            indexed ASC,
            name ASC
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    cursor.execute(query, arg_dict)
    artists: List[TDArtist] = cursor.fetchall()
    redis.set(redis_key, serialize_dict_list(artists), ex=600)
    lock.release()

    return artists


# def get_artists_by_name(pagination_init: PaginationInit, name: str = None, service: str = None, reload: bool = False) -> List[Artist]:

#     redis = get_conn()

#     if name and service:
#         key = f"artists_by_service_and_name:{service}:{name}"
#     elif name and not service:
#         key = f"artists_by_name:{name}"
#     else:
#         return get_artists(pagination_init, service=service, reload=reload)

#     artists = redis.get(key)

#     if artists and not reload:
#         return deserialize_dict_list(artists)

#     lock = KemonoRedisLock(redis, key, expire=60, auto_renewal=True)

#     if not lock.acquire(blocking=False):
#         time.sleep(0.1)
#         return get_artists_by_name(pagination_init, service=service, reload=reload)

#     cursor = get_cursor()
#     artist_count = count_artists(service)
#     pagination_db = PaginationDB(pagination_init, artist_count)
#     arg_dict = dict(
#         service=service,
#         name=name,
#         **pagination_db.get_info()
#     )

#     query = f"""
#         SELECT id, indexed, name, service, updated
#         FROM lookup
#         WHERE
#             service != 'discord-channel'
#             {f"AND service = %(service)s" if service else ""}
#             {f"AND name = %(name)s" if name else ""}
#         OFFSET %(offset)s
#         LIMIT %(limit)s
#     """

#     cursor.execute(query, arg_dict)
#     artists: List[Artist] = cursor.fetchall()
#     redis.set(key, serialize_dict_list(artists), ex=600)
#     return artists


# def validate_artists_request(requestArg: Request):
#     """
#     Validate parameters for artist search from request.
#     """
#     search_params: TDArtistListParams = requestArg.args.to_dict()
#     service = str(search_params["service"]).strip() if search_params.get("service") else None
#     page = int(search_params.get("page")) if search_params.get("page") else None
#     artist_name = str(search_params["name"]).strip() if search_params.get("name") else None
#     errors = []

#     if service and service not in paysite_list:
#         errors.append(dict(message=f"Invalid service parameter. Service must be one of {paysite_list}"))

#     if errors:
#         return ValidationResult(
#             is_successful=False,
#             validation_errors=errors
#         )

#     pagination_init = PaginationInit(page=page)
#     result_data = TDArtistListResult(
#         pagination_init=pagination_init,
#         name=artist_name
#     )

#     return ValidationResult(
#         is_successful=True,
#         data=result_data,
#     )
