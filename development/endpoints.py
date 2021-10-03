import requests
from flask import Blueprint, request, session, current_app, make_response, render_template

from configs.derived_vars import archiver_origin
from .internals import service_name
from .lib.test_accounts import register_test_accounts, write_test_accounts_data

from src.types.props import SuccessProps

development = Blueprint('development', __name__)

@development.get('/development')
def main_page():
    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'development/_index.html',
        props = props
    ), 200)
    return response

@development.post('/development')
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

@development.get('/development/test-entries')
def test_entries():
    props = dict(
        currentPage= 'development'
    )

    response = make_response(render_template(
        'development/test-entries.html',
        props = props
    ), 200)
    return response

@development.post('/development/test-entries')
def test_import():

    try:
        response = requests.post(
            f'{archiver_origin}/api/import',
            data = dict(
                service= service_name,
                session_key= request.form.get("session_key"),
                channel_ids= request.form.get("channel_ids"),
                save_session_key= request.form.get("save_session_key"),
                save_dms= request.form.get("save_dms"),
                contributor_id= session.get("account_id")
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
