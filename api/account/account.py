import elastic as elasticsearch
from smart_contract.eth import create_account as create_eth_account
from smart_contract.sawtooth import create_account as create_sawtooth_account
from utils.response import fail, success
from security import crypto
import logging


def create_account(body):
    password = body['password']
    username = body['username']
    user = elasticsearch.get_account_data(username)
    if user != {}:
        return fail("User existed")
    aes_key = crypto.fit_length(password)
    password = crypto.hash_password(password).hex()
    user_record = {
        "password": password,
        "username": username,
        "account_detail": {}
    }
    eth_address = ""
    if "eth_endpoint" in body:
        try:
            account = create_eth_account(body['eth_endpoint'])
        except Exception as e:
            return fail(e)
        private_key = account['private_key']
        eth_address = account['address']
        address = account['address']
        private_key = crypto.encrypt_private_key(aes_key,
                                                 private_key).hex()
        user_record["account_detail"]["etherum"] = {
            "public_key": address,
            "private_key": private_key,
            "endpoint_url": body['eth_endpoint']
        }
    if "sawtooth_endpoint" in body:
        try:
            account = create_sawtooth_account(body['sawtooth_endpoint'])
        except Exception as e:
            logging.warning(type(e))
            return fail(message=str(e))
        private_key = account['private_key']
        address = account['address']
        private_key = crypto.encrypt_private_key(aes_key,
                                                 bytes.fromhex(private_key)).hex()
        user_record["account_detail"]["sawtooth"] = {
            "public_key": address,
            "private_key": private_key,
            "endpoint_url": body['sawtooth_endpoint']
        }

    elasticsearch.create_user(user_record)
    return success("User created", address=eth_address)
