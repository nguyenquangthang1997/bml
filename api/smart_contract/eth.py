from web3 import Web3
import const
import uuid
import math
import threading
import json
from ipfs_handler import ipfs
from security import crypto
import logging

get_data_ = []


def create_account(infura_url):
    web3 = Web3(Web3.HTTPProvider(infura_url))
    account = web3.eth.account.create()
    address = account.address
    private_key = account.privateKey
    return {"address": address, "private_key": private_key}


def save_data(data_path, account, private_key, infura_url):
    account = Web3.toChecksumAddress(account)
    data_path_remain = data_path.copy()
    save_result = []
    path_tx_hashs = []
    web3 = Web3(Web3.HTTPProvider(infura_url))
    contract = web3.eth.contract(
        address=const.CONTRACT_ADDRESS,
        abi=const.CONTRACT_ABI)
    nonce = web3.eth.getTransactionCount(account)
    for i, path in enumerate(data_path):
        data = path
        index = str(uuid.uuid4())
        construct_txn = contract.functions.save_data(data, index).buildTransaction({
            'from': account,
            'nonce': nonce + i,
            'gas': 510800,
            'gasPrice': web3.eth.gasPrice * 3})

        signed = web3.eth.account.signTransaction(construct_txn, private_key)

        tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        path_tx_hashs.append({"path": path, "tx_hash": tx_hash, "id": index})
    for path_tx_hash in path_tx_hashs:
        try:
            transaction = web3.eth.waitForTransactionReceipt(transaction_hash=path_tx_hash['tx_hash'], timeout=360)
            if transaction['transactionHash'] == path_tx_hash['tx_hash']:
                data_path_remain.remove(path_tx_hash['path'])
                save_result.append(
                    {"data_path": path_tx_hash['path'], "transaction_id": path_tx_hash['id']})
            else:
                print("fail_save_eth")
                break
        except Exception as e:
            print("fail_save_eth")
            print(e)
            break
    return {"data_path": data_path_remain, "save_result": save_result}


def get_data(transaction_id, url, account):
    account = Web3.toChecksumAddress(account)
    web3 = Web3(Web3.HTTPProvider(url))
    data = web3.eth.contract(
        address=const.CONTRACT_ADDRESS,
        abi=const.CONTRACT_ABI)
    cid = data.functions.fetch_data(account, transaction_id).call()
    return cid
