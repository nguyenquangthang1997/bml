from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeSerializer as URLSafeSerializer


def generate_auth_token(secret_key, username, password):
    serializer = Serializer(secret_key, expires_in=15000)
    token = serializer.dumps({'username': username, "password": password})
    return token.decode()


def deserialize_auth_token(secret_key, token):
    serializer = Serializer(secret_key)
    return serializer.loads(token)


def generate_res_token(secret_key, body):
    serializer = URLSafeSerializer(secret_key)
    token = serializer.dumps(body)
    return token


def deserialize_res_token(secret_key, token):
    serializer = URLSafeSerializer(secret_key)
    return serializer.loads(token)
