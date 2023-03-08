from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from marshmallow import Schema, fields, post_load, exceptions
from marshmallow.exceptions import ValidationError
from flasgger import Swagger
from typing import List
import json

from word2med import Word2Med

# Init flask app
app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
}
api = Api(app)
swagger = Swagger(app)

# Init model
model = Word2Med()

# Init arg parser
parser = reqparse.RequestParser()

# Request Bodies
class VectorPayload(Schema):
    word = fields.Str()

class NeighboursPayload(Schema):
    word = fields.Str()
    n = fields.Integer()

class AnalogyPayload(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()
    
class Vector(Resource):
    def post(self):
        """
        Get the vector representation of a word
        ---
        parameters:
          - name: word
            in: body
            type: string
            required: true   
        """
        # Parse and validate post body
        try:
            schema = VectorPayload()
            payload = schema.loads(request.data)
        except ValidationError as e:
            return f"Invalid request body: {e}", 400

        # Get vector representation from model
        return model.get_vector(**payload), 200

class Neighbours(Resource):
    def post(self):
        """
        Get the n closest words to a word
        """
        # Parse and validate post body
        try:
            schema = NeighboursPayload()
            payload = schema.loads(request.data)
        except ValidationError as e:
            return f"Invalid request body: {e}", 400

        # Get n closest words from model
        return model.get_n_closest(**payload), 200

class Analogy(Resource):
    def post(self):
        """
        For words a, b, and c, get a list of words d which complete the analogy "a is to b as c is to d"
        """
        # Parse and validate post body
        try:
            schema = AnalogyPayload()
            payload = schema.loads(request.data)
        except ValidationError as e:
            return f"Invalid request body: {e}", 400
        
        # Get completed analogy from model
        return model.complete_analogy(**payload), 200

# Endpoint for each resource
api.add_resource(Vector, '/vector')
api.add_resource(Neighbours, '/neighbourhood')
api.add_resource(Analogy, '/analogy')

if __name__ == '__main__':
    app.run(debug=True)