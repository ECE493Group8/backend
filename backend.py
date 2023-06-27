import json
import logging
from typing import Dict

from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from flask_cors import CORS
from traceback import print_exc

from word2med import Word2Med
from schemas import *

MODELS_FILE = "./models.json"


# Init logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    filename='backend.log',
                    level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")
logging.info("Starting Word2Med API")


# Load model location (set in .env file)
with open(MODELS_FILE, "r") as f:
    model_paths = json.load(f)


# Init flask app
logging.info("Initializing Flask app...")
app = Flask(__name__)
app.config["API_TITLE"] = "Word2Med API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
CORS(app)
api = Api(app)
logging.info("Flask app initialized")


# Create blueprint
blp = Blueprint("word2med",
                "word2med",
                url_prefix="/",
                description=(
                    "Perform actions against the Word2Med model."
                    "Base URL: 129.128.215.93:5000"
                ))


# Init model
models: Dict[str, Word2Med] = {}
for model_id, model_path in model_paths.items():
    logging.info(f"Loading model '{model_id}'")
    models[model_id] = Word2Med(model_path)
    # Perform a query of the model to cache model data for faster future
    # queries.
    models[model_id].get_n_closest(["word"], n=10)
logging.info(f"Finished loading {len(models)} model(s)")


@blp.route('/vector')
class Vector(MethodView):
    @blp.arguments(VectorQuerySchema, location='query')
    @blp.response(200, VectorSchema)
    def get(self, args):
        """Get the vector representation of a word"""
        try:
            logging.info(f"Getting vector for word '{args['word']}' with model "
                         f"'{args['model']}'")
            model_id = args['model']
            return VectorSchema().load({
                'word': args['word'],
                'model': args['model'],
                'vector': models[model_id].get_vector(args['word']),
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

        For each input word, a list of the n closest words is returned, with the
        closest coming first.
        """
        try:
            logging.info(f"Getting neighbours for words {args['words']} with "
                         f"model {args['model']}")
            model_id = args['model']
            return NeighboursSchema().load({
                'words': args['words'],
                'n': args['n'],
                'model': args['model'],
                'neighbours': models[model_id].get_n_closest(args['words'],
                                                             args['n']),
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

        For words a, b, and c, get a list of n words d which complete the
        analogy "a is to b as c is to d"
        """
        try:
            logging.info(f"Getting analogy completions for words "
                         f"'{str(args['a'])}', '{str(args['b'])}', "
                         f"'{str(args['c'])}' with model '{args['model']}'")
            model_id = args['model']
            return AnalogySchema().load({
                'a': args['a'],
                'b': args['b'],
                'c': args['c'],
                'n': args['n'],
                'model': args['model'],
                'completions': models[model_id].complete_analogy(args['a'],
                                                                 args['b'],
                                                                 args['c'],
                                                                 args['n']),
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

        For the list of words, return a 2-dimensional embedding for each word
        and its neighbouring words.
        """
        try:
            logging.info(f"Getting embeddings for words {str(args['words'])} "
                         f"with model '{args['model']}'")
            model_id = args['model']
            words_list, embeddings_list = \
                    models[model_id].get_embeddings(args['words'], args['n'])
            return EmbeddingSchema().load({
                'words': args['words'],
                'n': args['n'],
                'model': args['model'],
                'words_list': words_list,
                'embeddings_list': embeddings_list,
            })
        except:
            print_exc()
            abort(500)


api.register_blueprint(blp)


# For debug purposes:
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')
