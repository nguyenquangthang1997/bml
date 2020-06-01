import json
import pandas as pd
import io
from elasticsearch import Elasticsearch
import pymysql
import requests
import lxml.etree as etree
import logging
# sys.path.append("../../api")
import elastic as elasticsearch
import helper
import math
import multiprocessing
from multiprocessing import Pool
from ipfs_handler import ipfs
from security import token as token_handler
import redis_handler.redis_interaction as res
import const
import xmltodict


def processor(user, mapping, is_save=True):
    if mapping['source']['data_type'] == "JSON":
        return json_processor(user=user, mapping=mapping, is_save=is_save)
    elif mapping['source']['data_type'] == "XLSX":
        return xlsx_processor(user=user, mapping=mapping, is_save=is_save)
    elif mapping['source']['data_type'] == "XML":
        return xml_processor(user=user, mapping=mapping, is_save=is_save)
    elif mapping['source']['data_type'] == "SQL":
        return sql_processor(user=user, mapping=mapping, is_save=is_save)
    elif mapping['source']['data_type'] == "ELASTIC_SEARCH":
        return elastic_processor(user=user, mapping=mapping, is_save=is_save)
    else:
        raise Exception("Invalid source data type. Currently, we only support JSON, XLSX, SQL, XML, ELASTIC_SEARCH")


def xlsx_processor(user, mapping, is_save):
    """
    :param username:
    :param mapping:
    :return:
    """
    username = user['username']
    mapping = pre_processing(username=username, mapping=mapping)
    iterator = mapping['source']['iterator']
    path = mapping['source']['path']
    try:
        res = requests.get(path)
        toread = io.BytesIO()
        toread.write(res.content)
        toread.seek(0)
    except:
        raise Exception("Invalid source path")

    datas = pd.read_excel(toread, sheet_name=iterator)
    row = datas.shape[0]
    datas = datas.to_json(orient="records")
    datas = json.loads(datas)
    number_record_in_file = math.ceil(len(datas) / (multiprocessing.cpu_count()))
    array = []
    for i in range(0, row, number_record_in_file):
        array.append((mapping, datas[i:i + number_record_in_file], user, is_save))
    p = Pool(len(array))
    data_to_save = p.map(xlsx_processing, array)
    p.close()
    p.join()
    return data_to_save


def xlsx_processing(params):
    record_temp = {}
    data_to_save = []
    mapping, datas, user, is_save = params
    # logging.warning(datas)
    for data in datas:
        for j in range(0, len(mapping['data_save'])):
            # logging.warning(data)
            # try:
            record_temp[mapping['data_save'][j]] = str(data[mapping['data_source'][j]])
            # except:
            #     raise Exception(
            #         "Reference attribute {atr} not appear in data source".format(atr=mapping['data_source'][j]))
        data_to_save.append(record_temp.copy())
    data_to_save = json_primary_linking(user=user, mapping=mapping, data_to_save=data_to_save)
    data_to_save = transform_function(mapping['function'], data_to_save)
    if is_save:
        suf_processing(user, mapping, data_to_save)
    return data_to_save


def json_processor(user, mapping, is_save):
    username = user['username']
    mapping = pre_processing(username=username, mapping=mapping)
    path = mapping['source']['path']
    try:
        res = requests.get(path)
        datas = json.loads(res.content.decode())
    except:
        raise Exception("Invalid source path")
    data_to_save = hierarchical_processor(mapping=mapping, user=user, datas=datas, is_save=is_save)
    return data_to_save


def recursive_xml(tree, iterator):
    if len(iterator) == 1:
        return etree.tostring(tree)
    else:
        result = []
        for tre in tree:
            if tre.tag == iterator[1]:
                b = recursive_xml(tre, iterator[1:])
                if type(b) is list:
                    result.extend(b)
                else:
                    result.append(b)
        return result


def xml_processor(user, mapping, is_save):
    username = user['username']
    mapping = pre_processing(username=username, mapping=mapping)
    path = mapping['source']['path']
    try:
        res = requests.get(path)
        tree = etree.fromstring(bytes(res.text, encoding='utf-8'))
        iterator_array = mapping['source']['iterator'].split(".")
        datas = recursive_xml(tree, iterator_array)
    except:
        raise Exception("Invalid source path")
    number_record_in_file = math.ceil(len(datas) / (multiprocessing.cpu_count()))
    array = []
    for i in range(0, len(datas), number_record_in_file):
        array.append((mapping, datas[i:i + number_record_in_file], user, is_save, iterator_array[-1]))
    p = Pool(len(array))
    data_to_save = p.map(hierarchical_xml_processing, array)
    p.close()
    p.join()
    return data_to_save


def hierarchical_processor(mapping, user, datas, is_save):
    iterator_array = mapping['source']['iterator'].split(".")
    if len(iterator_array) == 1 or iterator_array[0] == '':
        pass
    else:
        for iterator in iterator_array:
            datas = datas[iterator]
    number_record_in_file = math.ceil(len(datas) / (multiprocessing.cpu_count()))
    array = []
    for i in range(0, len(datas), number_record_in_file):
        array.append((mapping, datas[i:i + number_record_in_file], user, is_save))
    p = Pool(len(array))
    data_to_save = p.map(hierarchical_processing, array)
    p.close()
    p.join()
    return data_to_save


def hierarchical_xml_processing(params):
    record_temp = {}
    data_to_save = []
    mapping, datas, user, is_save, index = params
    for data in datas:
        data = xmltodict.parse(data)[index]
        try:
            for i in range(0, len(mapping['data_save'])):
                attribute_save_index = mapping['data_save'][i]
                attribute_save_index_array = attribute_save_index.split(".")
                attribute_source_index = mapping['data_source'][i]
                attribute_source_index_array = attribute_source_index.split(".")
                attribute_source_value = data
                for j in range(0, len(attribute_source_index_array)):
                    attribute_source_value = attribute_source_value[attribute_source_index_array[j]]
                cursor = record_temp
                for j in range(0, len(attribute_save_index_array) - 1):
                    if attribute_save_index_array[j] not in record_temp:
                        cursor[attribute_save_index_array[j]] = {}
                    cursor = cursor[attribute_save_index_array[j]]
                cursor[attribute_save_index_array[-1]] = attribute_source_value
            data_to_save.append(record_temp.copy())
        except Exception as e:
            logging.warning(e)
            raise Exception("Reference attribute {atr} not appear in data source".format(atr=e))
    data_to_save = json_primary_linking(user=user, mapping=mapping, data_to_save=data_to_save)
    data_to_save = transform_function(mapping['function'], data_to_save)
    if is_save:
        suf_processing(user, mapping, data_to_save)
    return data_to_save


def hierarchical_processing(params):
    record_temp = {}
    data_to_save = []
    mapping, datas, user, is_save = params
    for data in datas:
        try:
            for i in range(0, len(mapping['data_save'])):
                attribute_save_index = mapping['data_save'][i]
                attribute_save_index_array = attribute_save_index.split(".")
                attribute_source_index = mapping['data_source'][i]
                attribute_source_index_array = attribute_source_index.split(".")
                attribute_source_value = data
                for j in range(0, len(attribute_source_index_array)):
                    attribute_source_value = attribute_source_value[attribute_source_index_array[j]]
                cursor = record_temp
                for j in range(0, len(attribute_save_index_array) - 1):
                    if attribute_save_index_array[j] not in record_temp:
                        cursor[attribute_save_index_array[j]] = {}
                    cursor = cursor[attribute_save_index_array[j]]
                cursor[attribute_save_index_array[-1]] = attribute_source_value
            data_to_save.append(record_temp.copy())
        except Exception as e:
            logging.warning(e)
            raise Exception("Reference attribute {atr} not appear in data source".format(atr=e))
    data_to_save = json_primary_linking(user=user, mapping=mapping, data_to_save=data_to_save)
    data_to_save = transform_function(mapping['function'], data_to_save)
    if is_save:
        suf_processing(user, mapping, data_to_save)
    return data_to_save


def elastic_processor(user, mapping, is_save):
    username = user['username']
    mapping = pre_processing(username=username, mapping=mapping)
    data_to_save = []
    record_temp = {}
    path = mapping['source']['path'].split("/")
    try:
        es = Elasticsearch([{'host': path[0], 'port': path[1]}])
        count = es.count(index=mapping['source']['iterator'])
        count = count['count']
    except:
        raise Exception("Invalid source path")

    number_record_in_file = math.ceil(count / (multiprocessing.cpu_count()))
    array = []
    for i in range(0, count, number_record_in_file):
        array.append(
            (mapping, i, number_record_in_file, user, is_save, path[0], path[1], mapping['source']['iterator']))
    p = Pool(len(array))
    logging.warning(array)
    data_to_save = p.map(elastic_processing, array)
    p.close()
    p.join()
    return data_to_save


def elastic_processing(params):
    logging.warning(params)
    record_temp = {}
    data_to_save = []
    mapping, from_, size, user, is_save, host, port, index_name = params
    es = Elasticsearch([{'host': host, 'port': port}])
    datas = es.search(index=index_name, body={"query": {"match_all": {}}, "from": from_, "size": size},
                      request_timeout=200)
    datas = datas['hits']['hits']
    for data in datas:
        try:
            for i in range(0, len(mapping['data_save'])):
                attribute_save_index = mapping['data_save'][i]
                attribute_save_index_array = attribute_save_index.split(".")
                attribute_source_index = mapping['data_source'][i]
                attribute_source_index_array = attribute_source_index.split(".")
                attribute_source_value = data["_source"]
                for j in range(0, len(attribute_source_index_array)):
                    attribute_source_value = attribute_source_value[attribute_source_index_array[j]]
                cursor = record_temp
                for j in range(0, len(attribute_save_index_array) - 1):
                    if attribute_save_index_array[j] not in record_temp:
                        cursor[attribute_save_index_array[j]] = {}
                    cursor = cursor[attribute_save_index_array[j]]
                cursor[attribute_save_index_array[-1]] = attribute_source_value
            data_to_save.append(record_temp.copy())
        except Exception as e:
            raise Exception("Reference attribute {atr} not appear in data source".format(atr=e))

    data_to_save = json_primary_linking(user=user, mapping=mapping, data_to_save=data_to_save)
    data_to_save = transform_function(mapping['function'], data_to_save)
    if is_save:
        suf_processing(user, mapping, data_to_save)
    return data_to_save


def sql_processor(user, mapping, is_save):
    username = user['username']
    mapping = pre_processing(username=username, mapping=mapping)
    path = mapping['source']['path'].split("/")
    try:
        db = pymysql.connect(path[0], path[1], path[2], path[3])
        cursor = db.cursor()
        sql = "SELECT "
        for i in range(0, len(mapping['data_source'])):
            sql += "`" + mapping['data_source'][i] + "` "
            if i != len(mapping['data_source']) - 1:
                sql += ","
        sql += " FROM `" + mapping['source']['iterator'] + "`"

        cursor.execute(sql)
        datas = cursor.fetchall()
    except:
        raise Exception("Invalid source path")

    number_record_in_file = math.ceil(len(datas) / (multiprocessing.cpu_count()))
    array = []
    for i in range(0, len(datas), number_record_in_file):
        array.append((mapping, datas[i:i + number_record_in_file], user, is_save))
    p = Pool(len(array))
    data_to_save = p.map(sql_processing, array)
    p.close()
    p.join()
    return data_to_save


def sql_processing(params):
    data_to_save = []
    record_temp = {}
    mapping, datas, user, is_save = params
    for data in datas:
        try:
            for i in range(0, len(mapping['data_save'])):
                record_temp[mapping['data_save'][i]] = data[i]
            data_to_save.append(record_temp.copy())
        except Exception as e:
            raise Exception("Reference attribute {atr} not appear in data source".format(atr=e))
    data_to_save = json_primary_linking(user=user, mapping=mapping, data_to_save=data_to_save)
    data_to_save = transform_function(mapping['function'], data_to_save)
    if is_save:
        suf_processing(user, mapping, data_to_save)
    return data_to_save


def join_list_object(list1, list2, attribute1, attribute2):
    result = []
    dict1 = {}
    for i in range(0, len(list1)):
        dict1[str(list1[i][attribute1])] = []
    for i in range(0, len(list2)):
        dict1[str(list2[i][attribute2])] = []
    for i in range(0, len(list1)):
        dict1[str(list1[i][attribute1])].append(i)
    for i in range(0, len(list2)):
        dict1[str(list2[i][attribute2])].append(i)
    for value in dict1.values():
        if len(value) == 2:
            object_temp = list2[value[1]]
            del object_temp[attribute2]
            result.append({**list1[value[0]], **object_temp})
    return result


def json_primary_linking(user, mapping, data_to_save):
    username = user['username']
    for interlinking in mapping['interlinking']:
        index_name = interlinking['index_name']
        primary_data = interlinking['primary_data']
        if len(primary_data) == 2:
            temp_mapping = get_index_name(username=username, index_name=index_name)
            data_to_save_temp = processor(user=user, mapping=temp_mapping, is_save=False)
            data_to_save = join_list_object(data_to_save, data_to_save_temp, primary_data[0], primary_data[1])
    return data_to_save


# temp
def get_index_name(username, index_name):
    try:
        result = elasticsearch.get_index_name(username, index_name)
        return result['_source']
    except:
        raise Exception("Invalid identifier:{index_name} in linking".format(index_name=index_name))


def pre_processing(username, mapping):
    data_save = mapping['reference']
    data_save_temp = []
    source_temp = []
    interlinking = []
    for attribute in data_save:
        check_interlink = check_interlinking(attribute=attribute)
        if check_interlink['code'] == 2:
            mapping_temp = get_index_name(username=username, index_name=check_interlink['id'])
            mapping_temp = pre_processing(username=username, mapping=mapping_temp)
            data_save_temp.extend(mapping_temp['reference'])
            source_temp.extend(mapping_temp['reference'])
            interlinking.extend(mapping_temp['interlinking'])
        elif check_interlink['code'] == 1:
            interlinking.append({
                "id": check_interlink["id"],
                "primary_data": check_interlink["primary_data"]
            })
        else:
            temp_array = attribute.split("->")
            data_save_temp.append(temp_array[1])
            source_temp.append(temp_array[0])
    mapping['data_save'] = data_save_temp
    mapping['data_source'] = source_temp
    mapping['interlinking'] = interlinking
    return mapping


def check_interlinking(attribute):
    first = 0
    last = 0
    for i in range(0, len(attribute)):
        if attribute[i] == "(":
            first = i
        elif attribute[i] == ")":
            last = i
            break
    if first and last:
        if last - first == 1:
            return {"code": 2,
                    "id": attribute[0:first].replace(" ", ""),
                    "primary_data": []
                    }  # linking without primary
        else:
            primary_array = attribute[first + 1: last].replace(" ", "").split(",")
            return {"code": 1,
                    "id": attribute[0:first].replace(" ", ""),
                    "primary_data": primary_array
                    }  # linking with primary
    else:
        return {"code": 0,
                "id": "",
                "primary_data": []
                }  # not linking


def transform_function(transform_function, data_to_save):
    transform_array = []
    for transform in transform_function:
        transform_array_temp = transform.replace(" ", "").split("->")
        attribute_array = transform_array_temp[0].split(".")
        str_replace = "data"
        for attribute in attribute_array:
            str_replace += "['" + attribute + "']"
        if transform_array_temp[0] not in transform_array_temp[1]:
            raise Exception("Field {field} is not referred in function in declaration {declaration}".format(
                field=transform_array_temp[0], declaration=transform))
        transform_array_temp[1] = transform_array_temp[1].replace(transform_array_temp[0], str_replace)
        transform_array.append(transform_array_temp)
    for i, data in enumerate(data_to_save):
        for transform in transform_array:
            attribute_array = transform[0].split(".")
            cursor = data
            for attribute in attribute_array[:-1]:
                cursor = cursor[attribute]
            try:
                cursor[attribute_array[-1]] = eval(transform[1])
            except Exception as e:
                logging.warning(e)
                raise Exception("Error in declaration {declaration}".format(declaration=transform_function[i]))
    return data_to_save


def main(mapping, user):
    logging.warning(user)
    if mapping['blockchain'].upper() not in ['SAWTOOTH', "ETHERUM"]:
        raise Exception("Invalid blockchain type. Currently, we only support ETHERUM, SAWTOOTH ")
    processor(user=user, mapping=mapping, is_save=True)

    index_name = mapping['identifier']
    token_body = {
        'username': user['username'],
        "password": user['password'],
        "public_key": user['account_detail'][mapping['blockchain']]['public_key'],
        "private_key": user['account_detail'][mapping['blockchain']]['private_key'],
        "endpoint_url": user['account_detail'][mapping['blockchain']]['endpoint_url'],
        "type": mapping['blockchain'],
        "index_name": index_name}
    token = token_handler.generate_res_token(const.SECRET_KEY, token_body)
    cid = ipfs.stat(index_name + "_" + user['username'])
    res.add_mapping_synchronize_transaction(token, cid)


def suf_processing(user, mapping, data_to_save):
    index_name = mapping['identifier'] + "_" + user['username']
    user = {
        "password": user['password']
    }
    helper.save_data(user=user, datas=data_to_save, index_name=index_name)
