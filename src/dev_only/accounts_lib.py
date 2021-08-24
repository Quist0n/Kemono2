from ..internals.database.database import get_cursor
from ..lib.account import get_base_password_hash, is_username_taken

from datetime import datetime
import bcrypt
import hashlib


def generate_creds() -> dict[str, str]:
    seed = datetime.now().isoformat()
    username = seed + " " + get_base_password_hash(seed)
    password = seed
    return {'username': username, 'password': password}


def make_test_account() -> bool:

    creds = generate_creds()
    username = creds.get('username')
    password = creds.get('password')

    if is_username_taken():
        return False
    try:
        cursor = get_cursor()
        query = "INSERT INTO account (username, password_hash, role) values (%s, %s, 'tester');"
        password = bcrypt.hashpw(get_base_password_hash(password), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(query, (username, password))
        return True
    except:
        return False

def make_test_accounts(count:int) -> None:
    i = 0
    while i < count:
        make_test_account()
        i += 1
