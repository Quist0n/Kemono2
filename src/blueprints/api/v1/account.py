from flask import Blueprint, request, make_response, jsonify

from src.lib.account import load_account
from src.utils.utils import get_value
from src.lib.favorites import get_favorite_artists, get_favorite_posts


account_api = Blueprint('account_api', __name__, url_prefix='/account')

@account_api.route('/favorites', methods=['GET'])
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
