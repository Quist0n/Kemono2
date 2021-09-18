from flask import Blueprint, request, make_response, render_template, abort
# from datetime import datetime

from src.lib.administrator import get_account, get_accounts, change_account_role
from src.lib.account import load_account
from src.lib.pagination import Pagination

from typing import List
from src.types.account import visible_roles
from .types import Dashboard, Accounts, Role_Change

administrator = Blueprint(
    'admin',
    __name__
)

@administrator.before_request
def check_credentials():
    account = load_account()
    if (not account or account['role'] != 'administrator'):
        return abort(404)

@administrator.get('/administrator')
def get_admin():
    props = Dashboard()

    response = make_response(render_template(
        'administrator/dashboard.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@administrator.get('/administrator/accounts')
def get_accounts_list():
    queries = request.args.to_dict()
    queries['name'] = queries.get('name') if queries.get('name') else None

    # transform `role` query into a list for db query
    if queries.get('role') and queries.get('role') != 'all':
        queries['role'] = [queries['role']]
    else:
        queries['role'] = visible_roles

    pagination = Pagination(request)
    accounts = get_accounts(pagination, queries)
    props = Accounts(
        accounts= accounts,
        role_list= visible_roles,
        pagination= pagination
    )

    response = make_response(render_template(
        'administrator/accounts.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@administrator.post('/administrator/accounts')
def change_account_roles():
    form_dict = request.form.to_dict(flat=False)
    candidates = {
        # convert ids to `int`
        'moderator': [int(id) for id in form_dict.get('moderator')],
        'consumer': [int(id) for id in form_dict.get('consumer')]
    }

    if len(candidates['moderator']):
        change_account_role(candidates['moderator'], 'moderator', {
            'old_role': 'consumer',
            'new_role': 'moderator'
        })
    if len(candidates["consumer"]):
        change_account_role(candidates['consumer'], 'consumer', {
            'old_role': 'moderator',
            'new_role': 'consumer'
        })

    props = Role_Change()

    response = make_response(render_template(
        'success.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'

    return response


# @admin.route('/admin/accounts/<account_id>', methods= ['GET'])
# def get_account_info(account_id: str):
#     """
#     Detailed account page.
#     """
#     account = get_account(account_id)
#     props = admin_props.Account(
#         account= account
#     )

#     response = make_response(render_template(
#         'admin/account_info.html',
#         props = props,
#     ), 200)
#     response.headers['Cache-Control'] = 's-maxage=60'
#     return response

# @admin.route('/admin/accounts/<account_id>', methods= ['POST'])
# def change_account():
#     pass

# @admin.route('/admin/accounts/<account_id>/files')
# def get_account_files(account_id: str):
#     """
#     The lists of approved/rejected/queued files for the given account.
#     """
#     files = []
#     account = {}

#     props = admin_props.Account_Files(
#         account= account,
#         files= files
#     )
#     response = make_response(render_template(
#         'admin/account_files.html',
#         props = props,
#     ), 200)
#     response.headers['Cache-Control'] = 's-maxage=60'
#     return response

# @admin.route('/admin/mods/actions', methods= ['GET'])
# def get_moderators_audits():
#     """
#     The list of moderator actions.
#     """
#     actions = []
#     props = admin_props.ModeratorActions(
#         actions= actions
#     )
#     response = make_response(render_template(
#         'admin/mods_actions.html',
#         props = props,
#     ), 200)
#     response.headers['Cache-Control'] = 's-maxage=60'
#     return response
