from marshmallow import Schema, fields

class EmployeeSchema(Schema):
   id = fields.Int()
   name = fields.Str()
   city = fields.Str()
   country = fields.Str()
   salary = fields.Int()
   