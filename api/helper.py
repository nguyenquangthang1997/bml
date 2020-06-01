from jsonschema import validate
from jsonschema import ValidationError
from utils.response import fail, success
import uuid
import elastic as elasticsearch
import const
from security import token as token_handler
from security import crypto
import json
from ipfs_handler import ipfs
import redis_handler.redis_interaction as res
import logging
from multiprocessing import Pool
import math
import multiprocessing
import time


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            return fail(
                "'{}' parameter is required".format(field))


def validate_types(schema, body):
    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        string_array_error = str(e).split("\n")
        array = {"On instance", "[", "]", "'", ":", " "}
        for a in array:
            string_array_error[5] = string_array_error[5].replace(a, "")
        message = string_array_error[0] + " on field '" + string_array_error[5] + "'"

        return fail(message)


def save_data(user, datas, index_name, max_length=25000000):
    aes_key = crypto.fit_length(user['password'])
    data = json.dumps(datas)
    temp_string = crypto.encrypt(data, aes_key)
    cid = ipfs.add_bytes(temp_string)
    ipfs.cp(cid, index_name)
