from __future__ import absolute_import, unicode_literals

from .celery import app
import redis_handler.redis_interaction as res
import redis_handler.redis_handler as res_handler
import elastic
from smart_contract.controller import save_data

@app.task
def save_to_blockchain():
    redis_datas = res_handler.handle()
    for redis_data in redis_datas:
        path = redis_data['path']
        save_result = save_data(path, redis_data['token_dict'])
        save_failure = False
        for path_temp in save_result['data_path']:
            save_failure = True
            res.add_mapping_synchronize_transaction(redis_data['token'], path_temp)
        for save_result_data in save_result["save_result"]:
            transaction_id = save_result_data['transaction_id']
            elastic.add_transaction_id_to_mapping(redis_data['token_dict']['username'],
                                                  redis_data['token_dict']['index_name'], transaction_id)
        if save_failure:
            save_to_blockchain.delay()
