from flask import Blueprint, request, make_response, render_template, abort
from datetime import datetime

from ..utils.utils import limit_int

from ..lib.administrator import demote_moderators_to_consumers, get_account, get_accounts, promote_consumers_to_moderators
from ..lib.account import load_account
from ..lib.pagination import Pagination

from ..types.account import Account, account_roles
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

@admin.route('/admin/accounts', methods= ['GET'])
def get_accounts_list():
    pagination = Pagination(request)
    accounts = get_accounts(pagination)
    props = admin_props.Accounts(
        accounts= accounts,
        role_list= account_roles,
        pagination= pagination
    )

    response = make_response(render_template(
        'admin/accounts.html',
        props = props,
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@admin.route('/admin/accounts', methods= ['POST'])
def change_account_roles():
    print(request.form)
    candidates = {
        "moderator": [],
        "consumer": []
    }
    for role, account_id in request.form:
        if role in account_roles and role != "administrator":
            candidates[role].append(account_id)

    # promote_consumers_to_moderators(candidates["consumer"])
    # demote_moderators_to_consumers(candidates["moderator"])

    props = {
        'currentPage': 'admin'
    }
    response = make_response(render_template(
        'success.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'

    return response

# @admin.route('/admin/accounts/search', methods= ['POST'])
# def search_accounts():
#     """
#     Search results for accounts.
#     """
#     accounts = []
#     props = admin_props.Accounts(
#         accounts= accounts,
#         role_list= account_roles
#     )

#     response = make_response(render_template(
#         'admin/accounts.html',
#         props = props,
#     ), 200)
#     response.headers['Cache-Control'] = 's-maxage=60'
#     return response

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
