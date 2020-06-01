import redis

res = redis.Redis(host='redis-bml', port=6379, db=2)


def add_mapping_synchronize_transaction(account, path):
    res.rpush(account, *[path])


def get_mapping_synchronize_transaction(account):
    path = res.rpop(account)
    return path


def get_all_key():
    return res.keys()
