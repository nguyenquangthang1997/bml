from aiohttp.web import json_response
import traceback
import logging
import sys
from smart_contract.controller import get_data
import elastic as elasticsearch
import os
from utils.utils import decode_request, authorized
from utils.response import fail, success
from account.account import create_account as account_create
from worker.tasks import save_to_blockchain
import language.processor.controller as language_processor
import swagger
import bcrypt
from helper import validate_fields, validate_types
from security import token as token_handler
import const
import time
from ipfs_handler import ipfs


def exception_logging(exctype, value, tb):
    write_val = {'exception_type': str(exctype),
                 'message': str(traceback.format_tb(tb, 10))}
    logging.warn(str(write_val))


sys.excepthook = exception_logging
LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename="logFile.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


class Handler(object):

    def __init__(self):
        # self._dir = dir
        self.data_dir = os.getcwd() + "/data"
        super(Handler, self).__init__()

    @decode_request
    async def create_account(self, request, body, **kwargs):
        result = account_create(body=body)
        return result

    @decode_request
    @authorized
    async def synchronize(self, request, body, auth_user, **kwargs):
        file = open("result_test_file_size", "a")
        time_start = time.time()
        username = auth_user["username"]
        mappings = body['mapping']
        for mapping in mappings:
            existed_mapping = elasticsearch.get_index_name(username, mapping['identifier'])
            if existed_mapping != {}:
                return fail("Existed mapping")

        ids_ = elasticsearch.create_mapping_blockchain_mapping_record(username, mappings)
        try:
            for mapping in mappings:
                ipfs.mkdir(mapping['identifier'] + "_" + username)
            language_processor.processor(mappings, auth_user)
        except Exception as e:
            elasticsearch.delete_mapping_blockchain_mapping_record(ids_)
            for mapping in mappings:
                ipfs.rm(mapping['identifier'] + "_" + username)
            return fail(str(e))
        save_to_blockchain.delay()
        string = {"time": time.time() - time_start, "index": mappings[0]['identifier'],
                  "size": const.BLOCK_IPFS_SIZE, "type": "save"}
        file.writelines(str(string) + ", \n")
        return json_response(swagger.parse_swagger())

    @decode_request
    @authorized
    async def get_data(self, request, body, auth_user, **kwargs):
        file = open("result_test_file_size", "a")
        time_start = time.time()
        index_name = body.get("identifier")
        filter_condition = body.get("filter")
        mapping = elasticsearch.get_index_name(auth_user['username'], index_name)
        if mapping == {}:
            return fail("Wrong identifier")
        else:
            blockchain_type = mapping["_source"]["blockchain"]
        endpoint_url = auth_user["account_detail"][blockchain_type]["endpoint_url"]
        public_key = auth_user["account_detail"][blockchain_type]["public_key"]
        password = auth_user['password']
        transaction_id = mapping['_source']['transaction_id']
        condition = []
        for i in range(0, len(filter_condition)):
            condition.append(filter_condition[i].split("->"))
            attribute_array = condition[i][0].split(".")
            str_replace = "data"
            for attribute in attribute_array:
                str_replace += "['" + attribute + "']"
            condition[i][1] = condition[i][1].replace(condition[i][0], str_replace)
            if condition[i][0] not in condition[i][1]:
                return fail("Field {field} is not referred in filter in declaration {declaration}".format(
                    field=condition[i][0], declaration=filter_condition[i]))
        try:
            data_return = get_data(transaction_id, blockchain_type, endpoint_url, condition, public_key, password)
        except Exception as e:
            return fail(str(e))
        string = {"time": time.time() - time_start, "index": index_name, "size": const.BLOCK_IPFS_SIZE, "type": "get"}
        file.writelines(str(string) + ", \n")
        return success(data_return)

    @decode_request
    async def login(self, request, body, **kwargs):
        required_fields = ['username', 'password']
        validate_fields(required_fields, body)

        schema = {"type": "object", "properties": {"username": {"type": "string"}, "password": {"type": "string"}}}
        validate_types(schema, body)

        requested_password = bytes(body.get('password'), 'utf-8')

        user = elasticsearch.get_account_data(body.get('username'))
        if len(user) == 0:
            return json_response({'status': 'Failure',
                                  'statusCode': 2,
                                  'details': 'Username does not exist'})

        password = user['password']
        if not bcrypt.checkpw(requested_password, bytes.fromhex(password)):
            return json_response({'status': 'Failure',
                                  'statusCode': 4,
                                  'details': 'Wrong password'})

        token = token_handler.generate_auth_token(const.SECRET_KEY, user['username'], body.get('password'))
        public_key = user["account_detail"]["etherum"]['public_key']

        return success("Login successfully", authorization=token, public_key=public_key)
