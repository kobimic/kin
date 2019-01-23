import logging
import peewee
import config
import nexmo

from flask import make_response, jsonify, Blueprint, request
from models import User, Message, Plan
from schemas import SendMessageSchema, MessageSchema
from marshmallow import ValidationError



logging.basicConfig()
logger = logging.getLogger(__name__)
client = nexmo.Client(key=config.NEXMO_API_KEY, secret=config.NEXMO_API_SECRET)

messages_blueprint = Blueprint('resources.messages', __name__)
send_message_schema = SendMessageSchema()
message_schema = MessageSchema(many=True)


@messages_blueprint.route("/users/send", methods=['POST'])
def send_message():
    """ sending an sms message to a phone number,
        required body fields:
        {
            "email":"<email here>",
            "to":"972+<israeli mobile phone number>",
            "password":"<password here>"
            "message":"<message here..."
        }

        returned
        {
            "message": "messgae has been sent from <email> to <to>, your current balance is <current balance>"
        }
    """

    # simple input validation using marshmallow schemas
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'message': 'No input data provided'}), 400)
    try:
        data = send_message_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)

    # find the user, validate password and check its account for active

    user = User.select().where(User.email==data['email']).first()
    if not user:
        return make_response(jsonify({"message": "user account not valid, check email"}), 403)

    if user.verify_password(data['password']):
        if not user.is_verfied:
            return make_response(jsonify({"message": "user account is not verified, make sure your account is verified before sending messages"}), 403)

        if user.current_balance < user.plan.message_cost:
            return make_response(jsonify({"message": "user credit is not suffiecient, your balance is {} and message cost is {}".format(user.current_balance, user.plan.message_cost)}), 403)
        else:
            new_current_balance = user.current_balance - user.plan.message_cost
            client.send_message({
                'from': data['email'],
                'to': data['to'],
                'text': data["message"],
            })
            user.current_balance = new_current_balance
            user.save()
            Message.create(user=user, message=data["message"], to=data['to'])
            return make_response(jsonify({"message": "messgae has been sent from {} to {}, your current balance is {}".format(data['email'], data['to'], new_current_balance)}), 200)
    else:
        return make_response(jsonify({"message": "user account not valid, check email and passwword"}), 403)



@messages_blueprint.route("/users/messages", methods=['GET'])
def user_messsages():
    """ view user sms history ,
        required headers fields:
        "email":"<email here>",
        "verification_id":"<>verification_id here"

        returned:
        [
            {
                "created_at": "2019-01-23 21:20:30.690294",
                "message": "<message body....>",
                "to": "<phone number>"
            },
                        {
                "created_at": "2019-01-23 21:20:30.690294",
                "message": "<message body....>",
                "to": "<phone number>"
            },
        ]
    """
    email = request.headers.get('email')
    verification_id = request.headers.get('verification_id')
    if not (email and verification_id):
        return make_response(jsonify({'message': 'headers are missing email and/or verification_id'}), 403)

    user = User.select().where(User.email==email,User.verification_id==verification_id).first()
    if not user:
        return make_response(jsonify({'message': 'email and/or verification_id are invalid'}), 403)

    messages = Message.select().where(Message.user==user)    
    result = message_schema.dump(list(messages))
    return make_response(jsonify(result), 200)




