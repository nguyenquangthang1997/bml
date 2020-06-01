import requests
import json
import threading
import math
import const
import logging
from ipfs_handler import ipfs
from security import crypto

data_path_global = []
save_result_global = []
get_data_ = []


def get_data(transaction_id, account, url):
    url += "/get_data/" + str(transaction_id)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        response_content = json.loads(response.content)
        try:
            cid = response_content['data']
            return cid
        except Exception as e:
            logging.error(e)
            raise Exception(e)
    else:
        logging.error("get data from sawtooth error")
        logging.error("error" + str(response.reason) + " " + str(response.content))
        raise Exception("Get data from Sawtooth error")


def save_data(data_path, account, private_key, url):
    num_thread = const.NUMBER_THREAD
    count_transaction = math.ceil(len(data_path) / num_thread)
    global data_path_global
    global save_result_global
    data_path_global = data_path
    threads = []
    for i in range(0, len(data_path), count_transaction):
        a = threading.Thread(target=save_to_sawtooth_num_thread,
                             args=(data_path[i:i + count_transaction], account, private_key, url))
        a.start()
        threads.append(a)
    for thread in threads:
        thread.join()
    data_path_global_temp = data_path_global.copy()
    data_path_global = []
    save_result_global_temp = save_result_global.copy()
    save_result_global = []

    return {"data_path": data_path_global_temp, "save_result": save_result_global_temp}


def save_to_sawtooth_num_thread(data_path, account, private_key, url):
    for path in data_path:
        save_to_sawtooth(path, account, private_key, url)


def save_to_sawtooth(data_path, account, private_key, url):
    global data_path_global
    global save_result_global
    url += "/synchronize"
    data1 = {
        "public_key": account,
        "private_key": private_key,
        "data": data_path
    }
    response = requests.post(url, json=data1, verify=False)

    if response.status_code == 200:
        response_content = json.loads(response.content)
        try:
            print("success_save_sawtooth " + str(response_content['transaction_id']))
            data_path_global.remove(data_path)
            save_result_global.append(
                {"data_path": data_path, "transaction_id": str(response_content['transaction_id'])})
        except:
            print("fail_save_sawtooth")
    else:
        print("fail_save_sawtooth")


def create_account(url):
    url += "/user"
    try:
        response = requests.post(url, verify=False)
        if response.status_code == 200:
            try:
                response_content = json.loads(response.content)
                if response_content['public_key'] != "" and response_content['private_key'] != "":
                    return {"address": response_content['public_key'],
                            "private_key": response_content['private_key']}
            except:
                raise Exception(response.content.decode())
        raise Exception(response.reason)
    except:
        raise Exception("Invalid sawtooth endpoint url")
