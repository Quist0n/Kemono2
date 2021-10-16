from flask import Blueprint, g, redirect, url_for, make_response, render_template

from .pages import config

development = Blueprint('development', __name__)

@development.before_request
def check_creds():
    if not g.get('account'):
        return redirect(url_for('account.get_login'))

@development.get('/development')
def get_dev_page():
    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'development/home.html',
        props = props
    ), 200)
    return response

development.register_blueprint(config, url_prefix='/development')
