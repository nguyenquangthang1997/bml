import ipfshttpclient

api = ipfshttpclient.connect("/ip4/172.17.0.1/tcp/5001/http")
import logging


def add(path):
    result = api.add(path)
    return result['Hash']


def add_bytes(path):
    result = api.add_bytes(path)
    return result


def cat(cid):
    return api.cat(cid)


def mkdir(name):
    return api.files.mkdir("/{name}".format(name=name))


def cp(cid, dir_name):
    a = api.files.cp("/ipfs/{cid}".format(cid=cid), "/{dir_name}/{cid}".format(dir_name=dir_name, cid=cid))
    return 1


def rm(name):
    return api.files.rm("/{name}".format(name=name), recursive=True)


def stat(dir_name):
    return api.files.stat("/{dir_name}".format(dir_name=dir_name))['Hash']


def get_cid(p_cid):
    list_cid = []
    details = api.object.get(p_cid)
    for detail in details['Links']:
        list_cid.append(detail['Name'])
    return list_cid
