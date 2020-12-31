import requests
from core.url_mapper import get_url
import logging
from tqdm import tqdm
import time

def test_load_addretrieve():
    start = time.time()
    iterations = 100
    add_url = 'http://127.0.0.1:5000/add'
    add_map = dict()

    for _ in tqdm(range(iterations)):
        data = 'www.'+get_url()+'.com'
        payload = {'url': data}
        response = requests.post(add_url, json=payload)
        assert response.status_code == 200
        id_ = response.json()['tiny_url']
        add_map[id_] = data

    retrieve_url = 'http://127.0.0.1:5000/retrieve'

    for id_ in tqdm(add_map.keys()):
        response = requests.get(retrieve_url+'/'+id_)
        assert response.status_code == 200
        assert response.json().split()[-1] == add_map[id_]

    print(f'Inserting and retrieving {iterations} url took {time.time()-start} seconds')