from flask import Blueprint, g, redirect, url_for

from .pages import config

development = Blueprint('development', __name__)

@development.before_request
def check_creds():
    if not g.get('account'):
        return redirect(url_for('account.get_login'))

development.register_blueprint(config, url_prefix='/development')
