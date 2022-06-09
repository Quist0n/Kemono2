import datetime
import logging
import re
from datetime import timedelta
from os import getenv
from os.path import dirname, join
from threading import Lock
from urllib.parse import urljoin

from dotenv import load_dotenv
from flask import Flask, abort, g, redirect, render_template, request, session

import src.internals.cache.redis as redis
import src.internals.database.database as database
from configs.derived_vars import is_development
from src.internals.cache.flask_cache import cache
from src.lib.ab_test import get_all_variants
from src.lib.account import is_logged_in, load_account
from src.lib.notification import count_new_notifications
from src.blueprints import api, pages
from src.pages.account import account
from src.pages.artists import artists
from src.pages.dms import dms
from src.pages.favorites import favorites
from src.pages.help import help_app
from src.pages.imports import imports
from src.pages.legacy import legacy
from src.pages.post import post
from src.pages.posts import posts
from src.pages.random import random
from src.types.account import Account
from src.utils.utils import (
    freesites,
    paysite_list,
    paysites,
    paysite_options,
    render_page_data,
    url_is_for_non_logged_file_extension
)

load_dotenv(join(dirname(__file__), '.env'))


app = Flask(
    __name__,
    static_folder='dist/static',
    template_folder='dist/pages'
)

app.url_map.strict_slashes = False

app.register_blueprint(api)
app.register_blueprint(pages)
app.register_blueprint(legacy)
app.register_blueprint(artists)
app.register_blueprint(random)
app.register_blueprint(post)
app.register_blueprint(posts)
app.register_blueprint(account)
app.register_blueprint(favorites)
app.register_blueprint(dms)
app.register_blueprint(help_app, url_prefix='/help')
app.register_blueprint(imports)
if (is_development):
    from development import development
    app.register_blueprint(development)


app.config.from_pyfile('flask.cfg')
app.jinja_options = dict(
    trim_blocks=True,
    lstrip_blocks=True
)
app.jinja_env.globals.update(is_logged_in=is_logged_in)
app.jinja_env.globals.update(render_page_data=render_page_data)
app.jinja_env.filters['regex_match'] = lambda val, rgx: re.search(rgx, val)
app.jinja_env.filters['regex_find'] = lambda val, rgx: re.findall(rgx, val)

logging.basicConfig(filename='kemono.log', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

cache.init_app(app)
database.init()
redis.init()


@app.before_request
def do_init_stuff():
    g.page_data = {}
    g.request_start_time = datetime.datetime.now()
    g.freesites = freesites
    g.paysite_list = paysite_list
    g.paysites = paysites
    g.paysite_options = paysite_options
    g.origin = getenv("KEMONO_SITE")
    g.canonical_url = urljoin(getenv("KEMONO_SITE"), request.path)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)
    session.modified = False
    account = load_account()
    if account:
        g.account = Account.init_from_dict(account)
        g.new_notifications_count = count_new_notifications(g.account.id)


@app.after_request
def do_finish_stuff(response):
    if not url_is_for_non_logged_file_extension(request.path):
        start_time = g.request_start_time
        end_time = datetime.datetime.now()
        elapsed = end_time - start_time
        app.logger.debug('[{4}] Completed {0} request to {1} in {2}ms with ab test variants: {3}'.format(
            request.method, request.url, elapsed.microseconds / 1000, get_all_variants(), end_time.strftime("%Y-%m-%d %X")))
    response.autocorrect_location_header = False
    return response


@app.errorhandler(413)
def upload_exceeded(error):
    props = {
        'redirect': request.headers.get('Referer') if request.headers.get('Referer') else '/'
    }
    limit = int(getenv('REQUESTS_IMAGES')) if getenv('REQUESTS_IMAGES') else 1048576
    props['message'] = 'Submitted file exceeds the upload limit. {} MB for requests images.'.format(
        limit / 1024 / 1024
    )
    return render_template(
        'error.html',
        props=props
    ), 413


@app.teardown_appcontext
def close(e):
    # removing account just in case
    g.pop('account', None)
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
        connection = g.pop('connection', None)
        if connection is not None:
            try:
                pool = database.get_pool()
                connection.commit()
                pool.putconn(connection)
            except:
                pass
