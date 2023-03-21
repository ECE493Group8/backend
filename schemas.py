from marshmallow import Schema, fields

# Request Schemas

class VectorQuerySchema(Schema):
    word = fields.Str(required=True)

class NeighboursQuerySchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()

class AnalogyQuerySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()

class EmbeddingsQuerySchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()

# Response Schemas

class VectorSchema(Schema):
    word = fields.Str()
    vector = fields.List(fields.Float())

class NeighboursSchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    neighbours = fields.List(fields.List(fields.Tuple((fields.Str(), fields.Float()))))

class AnalogySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()
    completions = fields.List(fields.Tuple((fields.Str(), fields.Float())))

class EmbeddingSchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    words_list = fields.List(fields.Str())
    embeddings_list = fields.List(fields.List(fields.Float()))
