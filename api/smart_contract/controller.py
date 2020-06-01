from multiprocessing import Pool
import multiprocessing
import time
from smart_contract.eth import get_data as get_eth_data
from smart_contract.eth import save_data as save_eth_data
from smart_contract.sawtooth import get_data as get_sawtooth_data
from smart_contract.sawtooth import save_data as save_sawtooth_data
import logging
from ipfs_handler import ipfs
import json
from security import crypto


def save_data(data_path, account_data):
    if account_data['blockchain_type'] == "ETHERUM" or account_data['blockchain_type'] == "ETH":
        return save_eth_data(data_path, account_data['public_key'], account_data['private_key'],
                             account_data["endpoint_url"])
    elif account_data['blockchain_type'] == "SAWTOOTH":
        return save_sawtooth_data(data_path, account_data['public_key'], account_data['private_key'],
                                  account_data["endpoint_url"])


def get_data(transaction_id, blockchain_type, endpoint_url, condition, account, password):
    p_cid = get_blockchain_data(blockchain_type, endpoint_url, transaction_id, account)
    if p_cid == "":
        return_datas = [[]]
    else:
        cids = ipfs.get_cid(p_cid)
        array = []
        for cid in cids:
            array.append((cid, condition, password))
        p = Pool(len(array))
        return_datas = p.map(get_data_thread, array)
        p.close()
        p.join()
    for return_data in return_datas[1:]:
        return_datas[0].extend(return_data)
    return return_datas[0]


def get_data_thread(param):
    data_get_return = []
    cid, condition, password = param
    datas = ipfs.cat(cid)
    aes_key = crypto.fit_length(password)
    datas = crypto.decrypt(datas, aes_key).decode()
    datas = json.loads(datas)
    try:
        for data in datas:
            condition_flag = True
            for condition_temp in condition:
                condition_flag = condition_flag and eval(condition_temp[1])
                if not condition_flag:
                    break
            if condition_flag:
                data_get_return.append(data)
    except Exception as e:
        logging.warning("Filter error: " + str(e))
    return data_get_return


def get_blockchain_data(blockchain_type, endpoint_url, transaction_ids, account):
    if blockchain_type.upper() == "ETHERUM":
        return get_eth_data(transaction_ids, endpoint_url, account)
    elif blockchain_type.upper() == "SAWTOOTH":
        return get_sawtooth_data(transaction_ids, account, endpoint_url)
    else:
        return []
