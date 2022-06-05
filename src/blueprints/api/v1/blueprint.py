import math

from flask import Blueprint, jsonify, make_response, redirect, request, url_for

from src.lib.account import load_account
from src.lib.favorites import get_favorite_artists, get_favorite_posts
from src.utils.utils import get_value, parse_int

from .lib import count_artists, get_artists
from .types import DEFAULT_PAGE_LIMIT

v1api = Blueprint('v1', __name__, url_prefix='/v1')


@v1api.get("/account/favorites")
def list_account_favorites():
    account = load_account()
    if account is None:
        return {}, 401

    favorites = []
    fave_type = get_value(request.args, 'type', 'artist')
    if fave_type == 'post':
        favorites = get_favorite_posts(account['id'])
    else:
        favorites = get_favorite_artists(account['id'])

    results = favorites
    response = make_response(jsonify(results), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response


@v1api.get("/artists")
def get_artists_last():
    """
    A separate redirect page because blueprints
    cannot into path with undefined parameters.
    """
    limit = DEFAULT_PAGE_LIMIT
    artist_count = count_artists()
    total_pages = math.floor(artist_count / limit) + 1
    redirect_url = url_for('.list_artists', page=total_pages, **request.args)

    return redirect(redirect_url, 302)


@v1api.get("/artists/<page>")
def list_artists(page: str):
    current_page = parse_int(page)
    limit = DEFAULT_PAGE_LIMIT
    artist_count = count_artists()
    total_pages = math.floor(artist_count / limit) + 1
    is_valid_page = current_page and current_page <= total_pages
    # current page is zero or greater than total pages
    if (not is_valid_page):
        redirect_url = url_for('.list_artists', page=total_pages, **request.args)

        return redirect(redirect_url)

    offset = (current_page - 1) * limit
    sql_limit = artist_count - offset if current_page == total_pages else limit
    artists = get_artists(current_page, offset, sql_limit)

    response = make_response(jsonify(artists), 200)
    response.headers['Cache-Control'] = 's-maxage=60'

    return response
