from typing import List

from flask import Request

from src.internals.database.database import get_cursor

from .types import (
    Artist,
    PaginationDB,
    PaginationInit,
    TDArtistListParams,
    ValidationResult
)


def validate_artists_request(requestArg: Request):
    """"""
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
    errors = [dict(message="failed")]

    return ValidationResult(
        is_successful=False,
        data=result_data,
        validation_errors=errors
    )


def count_artists(service: str = None, name: str = None) -> int:
    """"""
    cursor = get_cursor()
    arg_dict = dict(
        service=service,
        name=name
    )
    query = f"""
        SELECT COUNT(*)
        FROM lookup
        WHERE
            service != 'discord-channel'
            {f"AND service = %(service)" if service else ""}
    """
    cursor.execute(query, arg_dict)
    artist_count: int = cursor.fetchone()[0]
    return artist_count


def get_artists(pagination_init: PaginationInit, service: str = None, name: str = None):
    """"""
    cursor = get_cursor()
    artist_count = count_artists(service, name)
    pagination_db = PaginationDB(pagination_init, artist_count)
    arg_dict = dict(
        service,
        **pagination_db
    )
    query = f"""
        SELECT id, indexed, name, service, updated
        FROM lookup
        WHERE
            service != 'discord-channel'
            {f"AND service = %(service)" if service else ""}
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    cursor.execute(query, arg_dict)
    artists: List[Artist] = cursor.fetchmany()
    return artists
