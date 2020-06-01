import datetime
from json.decoder import JSONDecodeError
import logging
import time
import base64
from aiohttp.web import json_response
from Crypto.Cipher import AES
import requests
import json
# defined in [[errors.py]]
from rest_api.errors import ApiBadRequest

# generated from **Protobuf**
from protobuf import payload_pb2
from google.protobuf.json_format import MessageToJson

LOGGER = logging.getLogger(__name__)


class RouteHandler(object):
    def __init__(self, loop, messenger):
        self._loop = loop
        self._messenger = messenger

    async def create_user(self, request):
        public_key, private_key = self._messenger.get_new_key_pair()
        encrypted_private_key = encrypt_private_key(
            request.app['aes_key'], public_key, private_key).hex()
        LOGGER.info(encrypted_private_key)
        return json_response({
            "public_key": public_key,
            "private_key": encrypted_private_key,
        })

    async def synchronize_data(self, request):
        body = await decode_request(request)
        public_key = body['public_key']
        encrypt_private_key = body['private_key']
        private_key = decrypt_private_key(request.app['aes_key'], public_key, encrypt_private_key)
        data = str(body['data'])
        LOGGER.info(data)
        transactionUnique = await self._messenger.send_synchronize_data_transaction(
            private_key=private_key,
            data=data
        )
        transactionUniqueId = transactionUnique.transactions[0].header_signature
        return json_response({
            "transaction_id": transactionUniqueId
        })

    async def get_data(self, request):
        transaction_id = request.match_info.get('transaction_id', '')
        url = "http://rest-api:8008/transactions/" + str(transaction_id)
        LOGGER.info(url)
        # url+=str(transaction_id)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                transaction_dict = json.loads(response.content)
                payload_string = transaction_dict['data']['payload']
                public_key = transaction_dict["data"]['header']['signer_public_key']
                data_model = payload_pb2.SimpleSupplyPayload()
                data_model.ParseFromString(base64.b64decode(payload_string))
                json_data = json.loads(MessageToJson(data_model, preserving_proto_field_name=True))
                return json_response({
                    "public_key": public_key,
                    "data": json_data['synchronize_data']['data']
                })
            except Exception as e:
                return json_response({'data': str(e)})
        return json_response({'data': ""})


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


def encrypt_private_key(aes_key, public_key, private_key):
    init_vector = bytes.fromhex(public_key[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    return cipher.encrypt(private_key)


def decrypt_private_key(aes_key, public_key, encrypted_private_key):
    init_vector = bytes.fromhex(public_key[:32])
    cipher = AES.new(bytes.fromhex(aes_key), AES.MODE_CBC, init_vector)
    private_key = cipher.decrypt(bytes.fromhex(encrypted_private_key))
    return private_key


def get_time():
    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)
