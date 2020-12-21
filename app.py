from flask import Blueprint, Flask
from views.api import api
from cassandra.cluster import Cluster

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    cluster = Cluster()
    session = cluster.connect()

    return app

app = create_app()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)