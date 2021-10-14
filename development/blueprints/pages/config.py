import requests
from flask import Blueprint, request, current_app, make_response, render_template, g, redirect, url_for

from configs.derived_vars import archiver_origin
from development.internals import service_name
from development.lib.test_accounts import register_test_accounts, write_test_accounts_data

from src.types.account import Account
from src.types.props import SuccessProps

config = Blueprint('config', __name__)

@config.get('/config')
def main_page():
    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'development/_index.html',
        props = props
    ), 200)
    return response

@config.post('/config')
def activate_dev_mode():
    accounts = register_test_accounts()
    print(f"Registered {len(accounts)} accounts.")
    is_saved = write_test_accounts_data(accounts)

    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'success.html',
        props = props
    ), 200)
    return response

@config.post('/config/service-keys')
def generate_service_keys():
    account: Account = g.account
    try:
        request = requests.post(
            url= f"{archiver_origin}/development/service-keys",
            data= dict(
                account_id = str(account.id)
            )
        )
        request.raise_for_status()
        props = SuccessProps(currentPage= 'dev-only', redirect= '/dev-only')

        response = make_response(render_template(
            'success.html',
            props = props
        ), 200)
        return response

    except Exception as e:
        current_app.logger.exception('Error connecting to archver')
        return f'Error while connecting to archiver. Is it running?', 500

@config.get('/config/test-entries')
def test_entries():
    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'development/test_entries.html',
        props = props
    ), 200)
    return response

@config.post('/config/test-entries')
def test_import():
    account: Account = g.account
    try:
        response = requests.post(
            f'{archiver_origin}/api/import',
            data = dict(
                service= service_name,
                session_key= request.form.get("session_key"),
                channel_ids= request.form.get("channel_ids"),
                save_session_key= request.form.get("save_session_key"),
                save_dms= request.form.get("save_dms"),
                contributor_id= account.id
            )
        )

        response.raise_for_status()
        import_id = response.text
        props = SuccessProps(
            currentPage= 'development',
            redirect= f'/importer/status/{import_id}{ "?dms=1" if request.form.get("save_dms") else "" }'
        )

        return make_response(render_template(
            'success.html',
            props = props
        ), 200)
    except Exception as e:
        current_app.logger.exception('Error connecting to archver')
        return f'Error while connecting to archiver. Is it running?', 500
