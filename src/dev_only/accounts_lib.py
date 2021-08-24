import string
import json
import os

from random import Random
from datetime import datetime

from configs.constants import test_path

from typing import Dict, List

acc_random = Random('Sneed')
username_vocabulary = string.ascii_letters + string.digits
password_vocabulary = string.ascii_letters + string.digits + string.punctuation

def make_test_accounts(count = 1000) -> List[Dict]:
    accounts = [generate_creds() for item in range(count)]

    return accounts

def generate_creds() -> Dict[str, str]:
    user = {
        'username': generate_random_string(5, 20, username_vocabulary, acc_random),
        'password': generate_random_string(10, 255, password_vocabulary, acc_random)
    }
    return user

def generate_random_string(min_length: int, max_length: int, vocabulary: str, random: Random = acc_random) -> str:
    string_length = random.randint(min_length, max_length)
    result_string = ''.join(random.choice(vocabulary) for char in range(string_length))

    return result_string

def create_accounts_json(accounts: List[Dict]) -> str:
    return json.dumps(accounts, indent=4)

def write_test_accounts_data(account_data: str) -> None:
    output_file = str(test_path) + "/accounts.json"
    if os.path.isdir(test_path) == False:
        os.mkdir(test_path)

    with open(output_file, 'wt') as f:
        f.write(create_accounts_json(account_data))
        f.close()
