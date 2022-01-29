from flask import Blueprint


from .account import account_api

v1api = Blueprint('v1', __name__, url_prefix='/v1')

v1api.register_blueprint(account_api)
