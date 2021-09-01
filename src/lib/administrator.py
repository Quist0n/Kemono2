from ..internals.database.database import get_cursor
from ..lib.pagination import Pagination
from ..lib.account import init_account_from_dict, init_accounts_from_dict

from typing import List
from ..types.account import Account, Moderator

def get_administrator():
    pass

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

def get_accounts(pagination: Pagination) -> List[Account]:
    cursor = get_cursor()
    query = """
        SELECT id, username, created_at, role 
        FROM account 
        ORDER BY 
            created_at DESC,
            username
        OFFSET %s 
        LIMIT %s;
        """
    cursor.execute(query, (pagination.offset, pagination.limit))
    accounts = cursor.fetchall()
    accounts = init_accounts_from_dict(accounts)

    return accounts

def search_accounts(pagination: Pagination, name: str) -> List[Account]:
    term = f"%%{name}%%"
    cursor = get_cursor()
    query = """
        SELECT id, username, created_at, role
        FROM account
        WHERE username LIKE %s
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
            pagination.offset, 
            pagination.limit
        )
    )
    accounts = cursor.fetchall()
    accounts = init_accounts_from_dict(accounts)
    
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

def get_moderator_actions():
    pass

def search_moderator_actions():
    pass
