from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time
import uuid
import logging



es = Elasticsearch([{"host": "elasticsearch", "port": "9200"}])

def create_blockchain_user_index():
    if not es.indices.exists(index="bml_user"):
        body = {
            "mappings": {
                "properties": {
                    "username": {"type": "keyword"},
                    "password": {"type": "text"},
                    "account_detail": {
                        "type": "object",
                        "properties": {
                            "etherum": {
                                "type": "object",
                                "properties": {
                                    "public_key": {"type": "keyword"},
                                    "private_key": {"type": "text"},
                                    "endpoint_url": {"type": "text"}
                                }
                            },
                            "sawtooth": {
                                "type": "object",
                                "properties": {
                                    "public_key": {"type": "keyword"},
                                    "private_key": {"type": "text"},
                                    "endpoint_url": {"type": "text"}
                                }
                            }
                        }
                    }
                }
            }
        }
        try:
            res = es.indices.create(index="bml_user", body=body)
            return res
        except Exception as e:
            print("already exist")


def create_mapping_blockchain_mapping_index():
    if not es.indices.exists(index="mapping_blockchain_mapping"):
        try:
            res = es.indices.create(index="mapping_blockchain_mapping")
            return res
        except Exception as e:
            print("already exist")


# def create_mapping_blockchain_transaction_index():
#     if not es.indices.exists(index="mapping_blockchain_transaction"):
#         try:
#             body = {
#                 "mappings": {
#                     "properties": {
#                         "account": {"type": "keyword"},
#                         "path": {"type": "keyword"},
#                         "index": {"type": "text"}
#                     },
#                 }, "settings": {
#                     "number_of_shards": 5,
#                     "number_of_replicas": 1,
#                     "max_result_window": 10000000,
#                     "mapping": {
#                         "total_fields": {
#                             "limit": "1000000"
#                         }
#                     }
#                 }
#             }
#             res = es.indices.create(index="mapping_blockchain_transaction", body=body)
#             return res
#         except Exception as e:
#             print("already exist")


create_blockchain_user_index()
create_mapping_blockchain_mapping_index()


# create_mapping_blockchain_transaction_index()


def get_account_data(username):
    body = {
        "query": {
            "match": {
                "username": username
            }
        }
    }
    res = es.search(index='bml_user', body=body, request_timeout=30)

    try:
        return res['hits']['hits'][0]['_source']
    except:
        return {}


def create_user(user_record):
    res = es.index(index='bml_user', doc_type='_doc', body=user_record, request_timeout=30)
    # log
    print(res)
    return {"result": res['result']}


def create_mapping_blockchain_mapping_record(account, mappings):
    ids_ = []
    for mapping in mappings:
        mapping['username'] = account
        res = es.index(index='mapping_blockchain_mapping', doc_type='_doc', body=mapping, refresh='wait_for',
                       request_timeout=30)
        ids_.append(res["_id"])
    return ids_
    # return {"result": res['result'], "account": account}


def delete_mapping_blockchain_mapping_record(ids_):
    for id_ in ids_:
        es.delete(index="mapping_blockchain_mapping", doc_type='_doc', id=id_,
                  request_timeout=30)


# def fetch_mapping(account):
#     body = {
#         "query": {
#             "match": {
#                 "username": account
#             }
#         }
#     }
#     res = es.search(index='mapping_blockchain_mapping', body=body, request_timeout=30)
#     try:
#         return res['hits']['hits'][0]
#     except:
#         return {}


def get_index_name(username, index_name):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "username": username
                        }
                    },
                    {
                        "match": {
                            "identifier": index_name
                        }
                    }
                ],
            }
        }
    }
    res = es.search(index='mapping_blockchain_mapping', body=body, request_timeout=30)
    try:
        return res['hits']['hits'][0]
    except:
        return {}


def add_transaction_id_to_mapping(username, index_name, transaction_id):
    mapping_saved_record = get_index_name(username, index_name)
    id = mapping_saved_record['_id']
    body = {
        "doc": {
            "transaction_id": transaction_id
        }
    }
    res = es.update(index='mapping_blockchain_mapping', id=id, body=body, request_timeout=30)
    return {"result": res['result']}
