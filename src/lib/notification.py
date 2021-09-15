from ..internals.database.database import get_cursor
from json import dumps

from typing import Dict, List

def send_notifications(account_ids: List[str], notification_type: int, extra_info: Dict[str,str]) -> bool:
    cursor = get_cursor()
    if  not account_ids:
        return False

    if extra_info is not None:
        extra_info = dumps(extra_info)
        notification_values = f'(%s, {notification_type}, \'{extra_info}\')'
    else:
        notification_values = f'(%s, {notification_type}, NULL)'

    insert_queries_values_template = ",".join([notification_values] * len(account_ids))
    insert_query = f"INSERT INTO notification (account_id, type, extra_info) VALUES {insert_queries_values_template}"
    cursor.execute(insert_query, account_ids)
    return True
