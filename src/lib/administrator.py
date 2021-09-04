from ..internals.database.database import get_cursor
from ..lib.pagination import Pagination
from ..lib.account import init_account_from_dict, init_accounts_from_dict

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
    term = f"%{queries['name']}%"
    cursor = get_cursor()
    query = """
        SELECT COUNT(*) AS total_number_of_accounts
        FROM account
        WHERE
            username LIKE %s
            AND role = ANY(%s)
        ;
    """
    cursor.execute(query, (
        term,
        queries['role'],
    ))
    result = cursor.fetchone()
    number_of_accounts = result['total_number_of_accounts']
    return number_of_accounts

def get_accounts(pagination: Pagination, queries: Dict[str, str]) -> List[Account]:

    arg_dict = {
            'role': queries['role'], # Role seem to not being parsed correctly, fix this
            'offset':pagination.offset,
            'limit':pagination.limit,
            }

    cursor = get_cursor()
    query = "SELECT id, username, created_at, role FROM account "
#    query += "WHERE role IN (%(role)s) "
#This is hardcoded, gotta fix
    query += "WHERE role IN ('consumer', 'moderator') "
    if queries['name'] is not None:
        arg_dict['username'] = f"%{queries['name']}%"
        query += "AND username LIKE %(username)s "

    query += "ORDER BY created_at DESC, username OFFSET %(offset)s LIMIT %(limit)s;"

    print(f"Role: {arg_dict['role']}")
    print(f"Args: {arg_dict}")
    print(f"Pre-execution Query: {query}")
    cursor.execute(query, arg_dict)
    accounts = cursor.fetchall()
    accounts = init_accounts_from_dict(accounts)

    count = count_accounts(queries)
    pagination.add_count(count)

    return accounts

def search_accounts(pagination: Pagination, queries: Dict[str, str]) -> List[Account]:
    query = """
        SELECT id, username, created_at, role
        FROM account
        WHERE
            username LIKE %s AND
            role = ANY(%s)
        ORDER BY
            created_at DESC,
            username
        OFFSET %s
        LIMIT %s;
        """
    cursor.execute(
        query,
        (
            term,
            queries['role'],
            pagination.offset,
            pagination.limit
        )
    )
    accounts = cursor.fetchall()
    total_count = count_total_search_results(queries)
    pagination.add_count(total_count)
    accounts = init_accounts_from_dict(accounts)
    return accounts

def count_total_search_results(queries: Dict[str, str]) -> int:
    term = f"%%{queries['name']}%%"
    cursor = get_cursor()
    query = """
        SELECT COUNT(*) AS total_number_of_accounts
        FROM account
        WHERE
            username LIKE %s AND
            role = ANY(%s)
        ;
    """
    cursor.execute(
        query,
        (
            term,
            queries['role'],
        )
    )
    number_of_accounts = cursor.fetchone().get('total_number_of_accounts')
    cursor.close()
    return number_of_accounts

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

def get_moderator_actions():
    pass

def search_moderator_actions():
    pass
