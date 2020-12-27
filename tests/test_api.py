import requests
from core.url_mapper import get_url
import logging

def test_add():
    add_url = 'http://127.0.0.1:5000/add'
    data = get_url()
    payload = {'url': 'www.'+data+'.com'}
    response = requests.post(add_url, json=payload)
    id_ = response.json()['tiny_url']

    retrieve_url = 'http://127.0.0.1:5000/retrieve'
    response = requests.get(retrieve_url+'/'+id_)
    assert response.status_code == 200
    assert response.json().split()[-1] == 'www.'+data+'.com'