from ..internals.database.database import get_cursor
from ..lib.pagination import Pagination
from ..lib.account import init_account_from_dict, init_accounts_from_dict
from ..lib.notification import send_notifications

from typing import Dict, List
from ..types.account import Account, Moderator

# def get_administrator():
#     pass

def get_account(account_id: str) -> Account:
    cursor = get_cursor()
    query = """
        SELECT id, username, created_at, role
        FROM account
        WHERE id = %s
        """
    cursor.execute(query, (account_id))
    account = cursor.fetchone()
    account = init_account_from_dict(account)

    return account


def count_accounts(queries: Dict[str, str]) -> int:

    arg_dict = {
        'role': queries['role'],
        'username': f"%%{queries['name']}%%" if queries.get('name') is not None else None
    }

    cursor = get_cursor()
    query = f"""
        SELECT COUNT(*) AS total_number_of_accounts
        FROM account
        WHERE
            role = ANY(%(role)s)
            {'AND username LIKE %(username)s' if queries.get('name') is not None else ''}
        ;
    """
    cursor.execute(query, arg_dict)
    result = cursor.fetchone()
    number_of_accounts = result['total_number_of_accounts']
    return number_of_accounts

def get_accounts(pagination: Pagination, queries: Dict[str, str]) -> List[Account]:

    arg_dict = {
        'role': queries['role'],
        'offset': pagination.offset,
        'limit': pagination.limit,
        'username': f"%%{queries['name']}%%" if queries.get('name') is not None else None
    }

    cursor = get_cursor()
    query = f"""
        SELECT id, username, created_at, role
        FROM account
        WHERE
            role = ANY(%(role)s)
            {'AND username LIKE %(username)s' if queries.get('name') is not None else ''}
        ORDER BY
            created_at DESC,
            username
        OFFSET %(offset)s
        LIMIT %(limit)s
        ;
    """

    cursor.execute(query, arg_dict)
    accounts = cursor.fetchall()
    accounts = init_accounts_from_dict(accounts)

    count = count_accounts(queries)
    pagination.add_count(count)

    return accounts

def promote_consumers_to_moderators(account_ids: List[str]):
    cursor = get_cursor()
    query = """
        UPDATE account
        SET role = \'moderator\'
        WHERE id = ANY (%s)
        ;
        """
    cursor.execute(query, (account_ids,))

    return True

def demote_moderators_to_consumers(account_ids: List[str]):
    cursor = get_cursor()
    query = """
        UPDATE account
        SET role = \'consumer\'
        WHERE id = ANY (%s)
        ;
        """
    cursor.execute(query, (account_ids,))

    return True

def change_account_role(account_ids: List[str], new_role: str, extra_info: dict):
    cursor = get_cursor()
    arg_dict = {
        "account_ids": account_ids,
        "new_role": new_role
    }


    change_role_query = """
        UPDATE account
        SET role = %(new_role)s
        WHERE id = ANY (%(account_ids)s)
        ;
        """
    cursor.execute(change_role_query, arg_dict)
    # TODO: Change notification_type (that 1) to whatever we use in future for account role changes
    send_notifications(account_ids, 1, extra_info)

    return True

def get_moderator_actions():
    pass

def search_moderator_actions():
    pass
