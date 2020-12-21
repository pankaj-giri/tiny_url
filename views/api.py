from flask import Blueprint, Flask, jsonify, request
from models.model import urlmap
from cassandra.cqlengine import connection
from core.url_mapper import get_url


api = Blueprint('api', __name__)

connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)

@api.route("/")
def index(path=None):
    return "Hello World"


@api.route("/add", methods=['GET', 'POST'])
def add_url():
    url = request.get_json()
    tiny = get_url()

    try:
        while True:
            # Continue regenerating until can insert successfully
            urlmap.get(tiny_url=tiny)
            print('Generated a key that already exists. Retrying...')
            tiny = get_url()
    except:
        print('Successfully generated a unique key - inserting into db..')

    url_object = urlmap.create(tiny_url=tiny, url=url['url'])
    url_object.save()
    return url_object.get_data()
