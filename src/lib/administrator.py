from ..internals.database.database import get_cursor
from ..lib.account import init_account_from_dict, init_accounts_from_dict

from ..types.account import Account

def get_administrator():
    pass

def get_accounts():
    cursor = get_cursor()
    query = 'SELECT * FROM account'
    cursor.execute(query)
    accounts = cursor.fetchall()
    accounts = init_accounts_from_dict(accounts)
    return accounts

def search_accounts():
    pass

def get_account_info(account_id: str) -> Account:
    cursor = get_cursor()
    query = 'SELECT 1 FROM account WHERE id = %s'
    cursor.execute(query, (account_id))
    account = cursor.fetchone()[0]
    account = init_account_from_dict()
    return account

def get_moderator_actions():
    pass

def search_moderator_actions():
    pass
