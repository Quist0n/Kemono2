from ..internals.database.database import get_cursor

def get_administrator():
    pass

def get_accounts():
    cursor = get_cursor()
    query = 'SELECT * FROM account'
    cursor.execute(query)
    accounts = cursor.fetchall()
    
    return accounts

def search_accounts():
    pass

def get_account_info():
    pass

def get_moderator_actions():
    pass

def search_moderator_actions():
    pass
