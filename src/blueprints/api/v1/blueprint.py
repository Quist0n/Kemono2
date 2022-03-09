from flask import Blueprint, jsonify, make_response, request


from src.lib.account import load_account
from src.lib.favorites import get_favorite_artists, get_favorite_posts
from src.utils.utils import get_value, parse_int
from .lib import get_artists, validate_artists_request

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
def list_artists():
    result = validate_artists_request(request)

    if (not result["is_successful"]):
        return make_response(jsonify(result["validation_errors"]), 422)

    artists = get_artists(
        pagination_init=result["data"]["pagination_init"]
    )

    response = make_response(jsonify(artists), 200)
    response.headers['Cache-Control'] = 's-maxage=60'

    return response
