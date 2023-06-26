from marshmallow import Schema, fields

# Request Schemas

class VectorQuerySchema(Schema):
    word = fields.Str(required=True)
    model = fields.Str(required=True)

class NeighboursQuerySchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    model = fields.Str(required=True)

class AnalogyQuerySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()
    model = fields.Str(required=True)

class EmbeddingsQuerySchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    model = fields.Str(required=True)

# Response Schemas

class VectorSchema(Schema):
    word = fields.Str()
    model = fields.Str(required=True)
    vector = fields.List(fields.Float())

class NeighboursSchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    model = fields.Str(required=True)
    neighbours = fields.List(fields.List(fields.Tuple((fields.Str(), fields.Float()))))

class AnalogySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()
    model = fields.Str(required=True)
    completions = fields.List(fields.Tuple((fields.Str(), fields.Float())))

class EmbeddingSchema(Schema):
    words = fields.List(fields.Str())
    n = fields.Integer()
    model = fields.Str(required=True)
    words_list = fields.List(fields.Str())
    embeddings_list = fields.List(fields.List(fields.Float()))
