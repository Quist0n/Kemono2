from flask import Blueprint, request, make_response, jsonify

from src.lib.account import load_account
from src.utils.utils import get_value, parse_int
from src.lib.favorites import get_favorite_artists, get_favorite_posts
from src.internals.database.database import get_cursor

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
def list():
    limit = parse_int(request.args.get('limit'), None) if request.args.get('limit') else None
    if (limit is None):
        query = "SELECT id, indexed, name, service, updated FROM lookup WHERE service != 'discord-channel'"
        cursor = get_cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    else:
        arg_dict = {'limit': limit}
        query = "SELECT id, indexed, name, service, updated FROM lookup WHERE service != 'discord-channel' LIMIT %(limit)s"
        cursor = get_cursor()
        cursor.execute(query, arg_dict)
        results = cursor.fetchall()

    response = make_response(jsonify(results), 200)
    response.headers['Cache-Control'] = 's-maxage=60'

    return response
