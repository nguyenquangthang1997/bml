import redis_handler.redis_interaction as res
import const
from security import token as token_handler
from security import crypto


# from helper import deserialize_auth_token, fit_lengh, decrypt_private_key, decrypt_public_key


def handle():
    result = []
    token_list = res.get_all_key()
    if len(token_list):
        for token in token_list:
            secret_key = const.SECRET_KEY
            token = token.decode("utf8")
            token_dict = token_handler.deserialize_res_token(secret_key, token)
            aes_key = crypto.fit_length(token_dict['password'])
            private_key = token_dict['private_key']
            public_key = token_dict['public_key']
            private_key = crypto.decrypt_private_key(aes_key, private_key).hex()
            token_dict = {
                "username": token_dict['username'],
                "index_name": token_dict['index_name'],
                "public_key": public_key,
                "private_key": private_key,
                "blockchain_type": token_dict['type'].upper(),
                "endpoint_url": token_dict['endpoint_url']
            }
            path = []
            path_temp = res.get_mapping_synchronize_transaction(token)
            while path_temp:
                path.append(path_temp.decode("utf-8"))
                path_temp = res.get_mapping_synchronize_transaction(token)
            result.append(
                {"path": path, "token": token, "token_dict": token_dict})
    return result
