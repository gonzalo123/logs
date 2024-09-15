import os
import json

import requests

from settings import LOG_DIR


def get_data(filename):
    with open(LOG_DIR / filename) as f:
        return {json.loads(line).get('hash'): json.loads(line) for line in f}


def get_not_published(ids):
    response = requests.post('http://localhost:5001/logs/api/check', json={'ids': ids})
    return response.json()



def persists(data):
    requests.post('http://localhost:5001/logs/api/persist', json=dict(ids=list(data.values())))
    return True


def publish_ids(data_to_publish, chunk_size=10):
    keys = list(data_to_publish.keys())
    for i in range(0, len(keys), chunk_size):
        chunk = keys[i:i + chunk_size]
        persists({k: data_to_publish[k] for k in chunk})


for file in os.listdir(LOG_DIR):
    if file.endswith('.json'):
        data = get_data(file)
        not_published = get_not_published(list(data.keys()))
        if len(not_published) == 0:
            os.remove(LOG_DIR / file)
        else:
            publish_ids({k: data[k] for k in not_published})
