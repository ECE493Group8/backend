from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from traceback import print_exc

from word2med import Word2Med
from schemas import *

# Init flask app
app = Flask(__name__)
app.config["API_TITLE"] = "Word2Med API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
api = Api(app)

# Create blueprint
blp = Blueprint("word2med", "word2med", url_prefix="/", description="Perform actions against the Word2Med model")

# Init model
model = Word2Med()

@blp.route('/vector')
class Vector(MethodView):
    @blp.arguments(VectorQuerySchema, location='query')
    @blp.response(200, VectorSchema)
    def get(self, args):
        """Get the vector representation of a word"""
        try:
            return VectorSchema().load({'word': args['word']})
        except Exception as e:
            print_exc()
            abort(500)

@blp.route('/neighbours')
class Neighbours(MethodView):
    @blp.arguments(NeighboursQuerySchema, location='query')
    @blp.response(200, NeighboursSchema)
    def get(self, args):
        """Get the most similar vectors to a word

        Returns a list of the n closest vectors to a given word, with the closest coming first.
        """
        try:
            return NeighboursSchema().load({
                'neighbours': model.get_n_closest(args['word'], args['n']),
                'n': args['n']
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
            return AnalogySchema().load(args | {'completions': model.complete_analogy(*args)})
        except:
            print_exc()
            abort(500)

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)