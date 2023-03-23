from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from traceback import print_exc
from dotenv import load_dotenv
import logging
import os

from word2med import Word2Med
from schemas import *

# Load model location (set in .env file)
load_dotenv()
MODEL_PATH = os.getenv('WORD2MED_MODEL_PATH')

# Init flask app
app = Flask(__name__)
app.config["API_TITLE"] = "Word2Med API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
api = Api(app)

# Create blueprint
blp = Blueprint("word2med", "word2med", url_prefix="/", description="Perform actions against the Word2Med model. Base URL: 129.128.215.93:5000")

# Init model
model = Word2Med(MODEL_PATH)

@blp.route('/vector')
class Vector(MethodView):
    @blp.arguments(VectorQuerySchema, location='query')
    @blp.response(200, VectorSchema)
    def get(self, args):
        """Get the vector representation of a word"""
        try:
            return VectorSchema().load({
                'word': args['word'],
                'vector': model.get_vector(args['word']),
            })
        except Exception as e:
            print_exc()
            abort(500)

@blp.route('/neighbours')
class Neighbours(MethodView):
    @blp.arguments(NeighboursQuerySchema, location='query')
    @blp.response(200, NeighboursSchema)
    def get(self, args):
        """From a list of words, get the most similar words to each of them

        For each input word, a list of the n closest words is returned, with the closest coming first.
        """
        try:
            return NeighboursSchema().load({
                'words': args['words'],
                'n': args['n'],
                'neighbours': model.get_n_closest(args['words'], args['n']),
            })
        except Exception as e:
            print_exc()
            abort(500)

@blp.route('/analogy')
class Analogy(MethodView):
    @blp.arguments(AnalogyQuerySchema, location='query')
    @blp.response(200, AnalogySchema)
    def get(self, args):
        """Get completions to an analogy

        For words a, b, and c, get a list of n words d which complete the analogy "a is to b as c is to d"
        """
        try:
            return AnalogySchema().load(args | {
                'a': args['a'],
                'b': args['b'],
                'c': args['c'],
                'n': args['n'],
                'completions': model.complete_analogy(**args),
            })
        except:
            print_exc()
            abort(500)

@blp.route('/embeddings')
class Embeddings(MethodView):
    @blp.arguments(EmbeddingsQuerySchema, location='query')
    @blp.response(200, EmbeddingSchema)
    def get(self, args):
        """Get the embeddings of words and their neighbours

        For the list of words, return a 2-dimensional embedding for each word and its neighbouring words.
        """
        try:
            words_list, embeddings_list = \
                    model.get_embeddings(args['words'], args['n'])
            return EmbeddingSchema().load({
                'words': args['words'],
                'n': args['n'],
                'words_list': args['words_list'],
                'embeddings_list': args['embeddings_list'],
            })
        except:
            print_exc()
            abort(500)

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')