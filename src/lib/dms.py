from typing import List
from ..internals.cache.redis import get_conn
from ..internals.database.database import get_cursor
from ..utils.utils import get_value
from ..types.kemono import DM
import ujson
import dateutil
import copy
import datetime
import base64

def get_unapproved_dms(import_id: str, reload: bool = False) -> List[DM]:
    redis = get_conn()
    key = 'unapproved_dms:' + import_id
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM unapproved_dms WHERE import_id = %s'
        cursor.execute(query, (import_id,))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 1)
    else:
        dms = deserialize_dms(dms)
    dms = init_DMs_from_dict(dms)
    return dms

def get_artist_dms(service: str, artist_id: int, reload: bool = False) -> List[DM]:
    redis = get_conn()
    key = 'dms:' + service + ':' + str(artist_id)
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM dms WHERE service = %s AND "user" = %s'
        cursor.execute(query, (service, artist_id))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 600)
    else:
        dms = deserialize_dms(dms)
    dms = init_DMs_from_dict(dms)
    return dms

def get_all_dms(offset: int, limit: int, reload: bool = False) -> List[DM]:
    redis = get_conn()
    key = 'all_dms:' + str(offset)
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM dms OFFSET %s LIMIT %s'
        cursor.execute(query, (offset, limit))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 600)
    else:
        dms = deserialize_dms(dms)
    dms = init_DMs_from_dict(dms)
    return dms

def get_all_dms_count(reload: bool = False) -> int:
    redis = get_conn()
    key = 'all_dms_count'
    count = redis.get(key)
    if count is None or reload:
        cursor = get_cursor()
        query = 'SELECT COUNT(*) FROM dms'
        cursor.execute(query)
        count = int(cursor.fetchone()['count'])
        redis.set(key, str(count), ex = 600)
    else:
        count = int(count)
    return count

def get_all_dms_by_query(q: str, offset: int, limit: int, reload: bool = False) -> List[DM]:
    redis = get_conn()
    key = 'all_dms_by_query:' + base64.b64encode(q.encode('utf-8')).decode('utf-8') + ':' + str(offset)
    dms = redis.get(key)
    if dms is None or reload:
        cursor = get_cursor()
        query = 'SELECT * FROM dms WHERE to_tsvector(\'english\', content) @@ websearch_to_tsquery(%s) OFFSET %s LIMIT %s'
        cursor.execute(query, (q, offset, limit))
        dms = cursor.fetchall()
        redis.set(key, serialize_dms(dms), ex = 600)
    else:
        dms = deserialize_dms(dms)
    dms = init_DMs_from_dict(dms)
    return dms

def get_all_dms_by_query_count(q: str, reload: bool = False) -> int:
    redis = get_conn()
    key = 'all_dms_by_query_count:' + base64.b64encode(q.encode('utf-8')).decode('utf-8')
    count = redis.get(key)
    if count is None or reload:
        cursor = get_cursor()
        query = 'SELECT COUNT(*) FROM dms WHERE to_tsvector(\'english\', content) @@ websearch_to_tsquery(%s)'
        cursor.execute(query, (q,))
        count = int(cursor.fetchone()['count'])
        redis.set(key, str(count), ex = 600)
    else:
        count = int(count)
    return count

def count_user_dms(service: str, user_id: str, reload: bool = False) -> int:
    redis = get_conn()
    key = f"dms_count:{service}:{user_id}"
    count = redis.get(key)
    if count is None or reload:
        cursor = get_cursor()
        query = 'SELECT COUNT(*) FROM dms WHERE service = %s AND "user" = %s'
        cursor.execute(query, (service, user_id))
        result = cursor.fetchall()
        count = result[0]['count']
        redis.set(key, str(count), ex = 600)
    else:
        count = int(count)
    return count

def cleanup_unapproved_dms(import_id: str):
    cursor = get_cursor()
    query = 'DELETE FROM unapproved_dms WHERE import_id = %s'
    cursor.execute(query, (import_id,))

    return True

def approve_dm(import_id: str, dm_id: str):
    cursor = get_cursor()
    query = 'INSERT INTO dms (id, "user", service, content, embed, added, published, file) SELECT id, "user", service, content, embed, added, published, file FROM unapproved_dms WHERE import_id = %s AND id = %s; '
    query += 'DELETE FROM unapproved_dms WHERE import_id = %s AND id = %s;'
    cursor.execute(query, (import_id, dm_id, import_id, dm_id))

    return True

def serialize_dms(dms):
    dms = copy.deepcopy(dms)
    return ujson.dumps(list(map(lambda dm: prepare_dm_fields(dm), dms)))

def deserialize_dms(dms_str):
    dms = ujson.loads(dms_str)
    return list(map(lambda dm: rebuild_dm_fields(dm), dms))

def rebuild_dm_fields(dm):
    dm['added'] = dateutil.parser.parse(dm['added'])
    dm['published'] = dateutil.parser.parse(dm['published'])
    return dm

def prepare_dm_fields(dm):
    dm['added'] = dm['added'].isoformat()
    dm['published'] = dm['published'].isoformat()
    return dm

def init_DMs_from_dict(dms: List[dict]) -> List[DM]:
    for index, dm in enumerate(dms):
        dms[index] = DM(
            id=dm["id"],
            user=dm["user"],
            service=dm["service"],
            content=dm["content"],
            added=dm["added"],
            published=dm["published"],
            embed=dm["embed"],
            file=dm["file"],
            import_id=dm.get("import_id") if dm.get("import_id") else None,
            contributor_id=dm.get("contributor_id") if dm.get("contributor_id") else None,
        )
    return dms
