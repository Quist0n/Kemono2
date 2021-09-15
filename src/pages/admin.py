from typing import List
from flask import Blueprint, request, make_response, render_template, abort
from datetime import datetime

from ..lib.administrator import get_account, get_accounts, change_account_role
from ..lib.account import load_account
from ..lib.pagination import Pagination

from ..types.account import visible_roles
from .admin_types import admin_props

admin = Blueprint(
    'admin',
    __name__
)

@admin.before_request
def check_credentials():
    account = load_account()
    if (not account or account['role'] != 'administrator'):
        return abort(404)

@admin.route('/admin')
def get_admin():
    props = admin_props.Dashboard()

    response = make_response(render_template(
        'admin/dashboard.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@admin.get('/admin/accounts')
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
    props = admin_props.Accounts(
        accounts= accounts,
        role_list= visible_roles,
        pagination= pagination
    )

    response = make_response(render_template(
        'admin/accounts.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@admin.post('/admin/accounts')
def change_account_roles():
    form_dict = request.form.to_dict(flat=False)
    candidates = {
        "moderator": convert_ids_to_int(form_dict.get('moderator')),
        "consumer": convert_ids_to_int(form_dict.get('consumer'))
    }

    # TODO: Change this line here and use the function as you see fit for this
    change_account_role(candidates["moderator"], 'moderator', None)
    props = {
        'currentPage': 'admin',
        'redirect': f"/admin/accounts"
    }

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

def convert_ids_to_int(list: List[str]):
    if list and len(list) != 0:
        return [int(item) for item in list]
