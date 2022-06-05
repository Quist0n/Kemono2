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


class TDArtistListResult(TypedDict):
    name: Optional[str]
    service: Optional[str]


class TDArtistResponse(TypedDict):
    artists: List[TDArtist]
