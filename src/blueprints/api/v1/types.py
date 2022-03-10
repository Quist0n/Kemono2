from datetime import datetime
from typing import Dict, List, Literal, Optional, TypedDict

from src.utils.utils import limit_int, parse_int

DEFAULT_PAGE_LIMIT = 25


class Artist(TypedDict):
    id: str
    indexed: datetime
    name: str
    service: str
    updated: datetime


class TDAPIRequest(TypedDict):
    """
    Base API request.
    For `GET` routes the keys are pulled from search params instead.
    """
    data: Optional[Dict]


class TDAPIResponseSuccess(TypedDict):
    """
    Base API response.

    """
    is_successful: Literal[True]
    data: Optional[Dict]


class TDAPIResponseFaillure(TypedDict):
    """
    `validation_errors` is a separate entity for use by forms.
    """
    is_successful: Literal[False]
    errors: Optional[List[str]]
    validation_errors: Optional[List[Dict]]


class TDArtistListParams(TypedDict):
    page: int
    service: str
    name: str


class ValidationResult(TypedDict):
    """
    TODO: Rewrite as a class with a generic.
    """
    is_successful: bool
    data: Optional[Dict]
    validation_errors: Optional[List[Dict]]


class PaginationInit:
    """
    Pagination stats collected from request.
    """

    def __init__(self, page: int = 1) -> None:
        """
        The absence of `page` value means the last page.
        """
        self.page = parse_int(page, 1)
        self.limit = DEFAULT_PAGE_LIMIT


class PaginationDB:
    """
    Pagination stats for database query.
    """

    def __init__(self, pagination_init: PaginationInit, total_count: int) -> None:
        self.total_count = total_count
        self.offset = self.calculate_offset(pagination_init.page, total_count)
        self.limit = self.calculate_limit(total_count, self.offset)

    def calculate_offset(self, page: int, total_count: int):
        offset = (page - 1) * DEFAULT_PAGE_LIMIT

        # something-something offset should not be higher than total count
        if (offset > total_count):
            offset = total_count

        return offset

    def calculate_limit(self, total: int, offset: int):
        """
        The sql `LIMIT` value.
        """
        limit = limit_int(total - offset, DEFAULT_PAGE_LIMIT)
        return limit

    def get_info(self) -> dict:
        return dict(
            offset=self.offset,
            limit=self.limit
        )


class PaginationClient:
    """
    Pagination stats for client, paginator component specifically.
    """

    def __init__(self, pagination_db: PaginationDB) -> None:
        self.current_page = 0
        self.total_count = 0
        self.current_count = self.calculate_current_count()

    def calculate_total_pages():
        """"""

    def calculate_current_count():
        """
        @TODO
        """
        # current_count_min = 0
        # current_count_max = 0


class TDArtistListResult(TypedDict):
    pagination_init: PaginationInit
    name: Optional[str]
    service: Optional[str]


class TDArtistResponse(TypedDict):
    artists: List[Artist]
    pagination_client: PaginationClient
