from cassandra.cqlengine import columns
from models.base import Base
from flask import jsonify

class urlmap(Base):
    tiny_url = columns.Text(primary_key=True)
    url = columns.Text()

    def get_data(self):
        return jsonify({
            'tiny_url' : self.tiny_url,
            'url' : self.url
        })