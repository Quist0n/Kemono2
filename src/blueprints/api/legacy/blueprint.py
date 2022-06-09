from flask import Blueprint, request, redirect, url_for, make_response, jsonify

from src.internals.database.database import get_cursor
legacy_api = Blueprint('legacy_api', __name__)


@legacy_api.get('/favorites')
def api_list():
    new_url = url_for('api.v1.list_account_favorites', **request.args)
    return redirect(new_url, 301)


# @TODO: deprecate once server name search is in place
@legacy_api.route('/api/creators')
def creators():
    # new_url = url_for('api.v1.list_artists', **request.args)
    # return redirect(new_url, 301)
    cursor = get_cursor()
    query = "SELECT * FROM lookup WHERE service != 'discord-channel'"
    cursor.execute(query)
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)
