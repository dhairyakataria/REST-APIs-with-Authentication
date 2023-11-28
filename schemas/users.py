from enum import Enum
from marshmallow import Schema, fields

# Enum to define user roles
class Role(Enum):
    user = 'user',
    admin = 'admin'

# Schema for user data
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    Username = fields.Str(required=True)
    Email = fields.Email(required=True)
    U_password = fields.String(required=True, load_only=True)
    Role = fields.String(required=True, default='User')

# Schema for querying user data
class UserQuerySchema(Schema):
    id = fields.Int(required=True)

# Schema for success messages
class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)

# Schema for user login data
class LoginSchema(Schema):
    Username = fields.Str(required=True)
    U_password = fields.Str(required=True)
