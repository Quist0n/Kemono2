from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Literal, Optional, TypedDict


DEFAULT_PAGE_LIMIT = 25


class TDArtist(TypedDict):
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
    errors: List[str]


class TDArtistListParams(TypedDict):
    service: Optional[str]
    # name: str


class ValidationResult(TypedDict):
    """
    TODO: Rewrite as a class with a generic.
    """
    is_successful: bool
    data: Optional[Dict]
    validation_errors: Optional[List[Dict]]


class TDPaginationDB(TypedDict):
    current_page: int
    offset: int
    sql_limit: int


class TDPagination(TypedDict):
    total_count: int
    total_pages: int
    current_page: int
    limit: int


class TDArtistResponse(TypedDict):
    pagination: TDPagination
    artists: List[TDArtist]
