from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import bcrypt
import Crypto.Util.Counter
import os.path, struct
import const
import logging

BLOCK_SIZE = const.BLOCK_SIZE
PADDING = const.PADDING
ctr = Crypto.Util.Counter.new(128)


def decrypt_private_key(aes_key, encrypted_private_key):
    cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)
    private_key = cipher.decrypt(bytes.fromhex(encrypted_private_key))
    return private_key


def encrypt_private_key(aes_key, private_key):
    cipher = AES.new(aes_key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(private_key)


def fit_length(init_vector):
    init_vector = init_vector.encode()
    init_vector = SHA256.new(init_vector).digest()
    return init_vector


def hash_password(password):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def encrypt(content, key):
    try:
        content = content.encode()
        # file_size = len(content)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        encrypted_content = cipher.encrypt(content)
    except Exception as e:
        logging.warning(str(e))
    # encrypted_content = struct.pack('<Q', file_size)
    # start = 0
    # while True:
    #     block = content[start:start + BLOCK_SIZE]
    #     start = start + BLOCK_SIZE
    #     if len(block) % 16 != 0:
    #         block += (PADDING * (16 - len(block) % 16)).encode()
    #     elif len(block) == 0:
    #         break
    #     encrypted_content += cipher.encrypt(block)
    return encrypted_content


def decrypt(content, key):
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    result = cipher.decrypt(content)
    # size = struct.unpack('<Q', content[:struct.calcsize('Q')])[0]
    # start = struct.calcsize('Q')
    # result = b""
    # while True:
    #     block = content[start:start + BLOCK_SIZE]
    #     start = start + BLOCK_SIZE
    #     if len(block) == 0:
    #         break
    #     result += cipher.decrypt(block)
    # result = result[:size]
    return result
