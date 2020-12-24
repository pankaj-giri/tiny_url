from flask import Blueprint, Flask, jsonify, request
from models.model import urlmap
from core.url_mapper import get_url


api = Blueprint('api', __name__)

@api.route("/")
def index(path=None):
    return "Hello World"



@api.route("/add", methods=['GET', 'POST'])
def add_url():
    url = request.get_json()
    print(url)
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
    print('inserted : ', urlmap.get(tiny_url=tiny))
    url_object.save()
    return url_object.get_data()


@api.route("/retrieve/<id>", methods=['GET'])
def retrieve(id):
    print(f'Short url id to retrieve : {id}')
    results = urlmap.objects.filter(tiny_url=id)

    if len(results) == 0:
        return f"No results found for id : {id}"

    for instance in results:
        result = instance.url
    
    return f"URL for id {id} is {result}"

