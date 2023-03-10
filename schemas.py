from marshmallow import Schema, fields

# Request Schemas

class VectorQuerySchema(Schema):
    word = fields.Str(required=True)

class NeighboursQuerySchema(Schema):
    word = fields.Str()
    n = fields.Integer()

class AnalogyQuerySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()

# Response Schemas

class NeighboursSchema(Schema):
    word = fields.Str()
    n = fields.Integer()
    neighbours = fields.List(fields.Str())

class VectorSchema(Schema):
    word = fields.Str()
    # TODO: Add fields describing vector representation of a word

class AnalogySchema(Schema):
    a = fields.Str()
    b = fields.Str()
    c = fields.Str()
    n = fields.Integer()
    completions = fields.List(fields.Str())