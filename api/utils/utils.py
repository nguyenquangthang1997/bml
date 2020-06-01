import json
import logging
import const
from security import token as token_handler
from utils.response import fail, success
from itsdangerous import BadSignature
import elastic as elasticsearch


def decode_request(func):
    async def fun(*args, **kwargs):
        if args[1].headers["Content-Type"].lower() == "application/json":
            try:
                body = await args[1].json()
            except:
                return fail("Improper json format")
        else:
            data = await args[1].post()
            body = data.get("mapping").file.read()
            body = json.loads(body.decode())
        kwargs['body'] = body
        return await func(*args, **kwargs)

    return fun


def authorized(func):
    async def fun(*args, **kwargs):
        token = args[1].headers.get('AUTHORIZATION')
        if token is None:
            return fail('No auth token provided')
        token_prefixes = ('Bearer', 'Token')
        for prefix in token_prefixes:
            if prefix in token:
                token = token.partition(prefix)[2].strip()
        try:
            token_dict = token_handler.deserialize_auth_token(const.SECRET_KEY, token)
        except BadSignature:
            return fail('Invalid auth token')
        username = token_dict.get('username')
        password = token_dict.get('password')

        user = elasticsearch.get_account_data(username)
        if len(user) == 0:
            return fail('Token is not associated with an user')
        user['password'] = password
        kwargs['auth_user'] = user
        return await func(*args, **kwargs)

    return fun
