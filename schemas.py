from marshmallow import Schema, fields, validate, pre_load, post_dump, post_load, ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class UserSchema(Schema):
    email = fields.Str(required=True,validate=validate.Email(error='Not a valid email address'))
    password = fields.Str(required=True,validate=[validate.Length(min=8, max=20)])
    mobile = fields.Str(required=True, validate=[validate.Length(min=9, max=10)])


class UserInfoSchema(Schema):
    email = fields.Str()
    mobile = fields.Str()
    is_verfied = fields.Str()
    current_balance = fields.Str()



class VerifySchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(
            error='Not a valid email address'))
    verification_id = fields.Str(required=True, validate=[validate.Length(min=32, max=32)])
    code = fields.Str(required=True, validate=[validate.Length(min=4, max=6)])


class SendMessageSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(
        error='Not a valid email address'))
    password = fields.Str(required=True, validate=[
                          validate.Length(min=8, max=20)])
    to = fields.Str(required=True, validate=[
                        validate.Length(min=9, max=13)])
    message = fields.Str(required=True, validate=[
        validate.Length(min=1, max=140)])


class MessageSchema(Schema):

    to = fields.Str(required=True, validate=[
        validate.Length(min=9, max=13)])
    message = fields.Str(required=True, validate=[
        validate.Length(min=1, max=140)])
    created_at = fields.Str(required=True)

