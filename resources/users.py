import logging
import peewee
import config
import nexmo

from flask import make_response, jsonify, Blueprint, request
from models import User, Message, Plan
from schemas import UserSchema, VerifySchema, UserInfoSchema
from marshmallow import ValidationError



logging.basicConfig()
logger = logging.getLogger(__name__)
client = nexmo.Client(key=config.NEXMO_API_KEY, secret=config.NEXMO_API_SECRET)

users_blueprint = Blueprint('resources.users', __name__)
user_schema = UserSchema()
verify_user_schema = VerifySchema()
user_info_schema = UserInfoSchema()



@users_blueprint.route("/users/register", methods=['POST'])
def register_user():
    """ register a new user, 
        required body fields:
        {
	        "email":"<email here>",
	        "mobile":"<israeli mobile phone number>",
	        "password":"<password>"
        }
        
        returned 
        {
        "email": "<email address",
        "verification_id": "<verification id>"
        }
    """

    # simple input validation using marshmallow schemas
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'message': 'No input data provided'}), 400)
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)

    # check to see if user already exist, if so return
    user = User.select().where(User.email == data['email']).first()
    if user:
        return make_response(jsonify({"message": "error registering, user already exist"}), 403)

    try:
        # setting up the user...
        # get the default plan for credit and message cost
        plan, created = Plan.get_or_create(title="regular")
        data['plan'] = plan
        # set the initial plan balance as the neww user current balance
        data['current_balance'] = plan.initial_balance

        # get a verfication code from nexmo, and store the trans id in the users table (or redis...)
        # the api request for nexmo is using a 4 digit default code, and i've configured it for IL for convenience (shorter numbers...)
        response = client.start_verification(number=data["mobile"], brand="kin", country="IL", )
        if response["status"] == "0":
            logger.info("Started verification request_id is {}".format(response["request_id"]))
        else:
            logger.error(response["error_text"])
            return make_response(jsonify({"message": "could not send verification code, please contact admin"}), 500)

        # set the trans id in the users table
        data["verification_id"]=response["request_id"]
        # set the password as hashed
        data["password"] = User.set_password(data["password"])
        # create the user using the values given above
        User.create(**data)
        return make_response(jsonify({"email": data["email"], "verification_id": response["request_id"]}), 200)
    except peewee.IntegrityError:
        return make_response(jsonify({"message": "error registering user"}), 403)




@users_blueprint.route("/users/verify", methods=['POST'])
def verify_user():
    """ verifing a registered user,
        required body fields:
        {
            "email":"<email here>",
            "verification_id":"<the long code/verification code that was returned from the registeration request>",
            "code":"<the code you got over the phone>"
        }

        returned
        {
            message...and status code
        }
    """

    # simple input validation using marshmallow schemas
    json_data=request.get_json()
    if not json_data:
        return make_response(jsonify({'message': 'No input data provided'}), 400)
    try:
        data = verify_user_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)

    try:
        # check to see if a user is already, verified if so, return
        user = User.get(User.email == data['email'])
        if user.is_verfied:
            return make_response(jsonify({"message": "error, user is already verfied"}), 403)
    except peewee.DoesNotExist:
        return make_response(jsonify({"message": "error, user does not exist"}), 403)

    # if you are here, it means that the user exist and not verified
    try:
        # check a verfication code with nexmo using the trans_id given to you upon registering and the code given to you using sms
        response = client.check_verification(data["verification_id"], code=data["code"])
        if response["status"] == "0":
            logger.info("verification passed for id {}, event_id={}".format(
                data["verification_id"], response['event_id']))
            # update the user with the matching trans_id and the matching email to become active, in order to send sms messages
            query = User.update(is_verfied=True).where(
                User.verification_id == data["verification_id"], User.email == data["email"])
            query.execute()
            return make_response(jsonify({"message": "user has been verfied"}), 200)
        else:
            logger.error(response["error_text"])
            return make_response(jsonify({"message": "could not verify code, make sure you've entered the right codde, or try registering again"}), 500)

    except Exception as err:
        logger.error(err.message)
        return make_response(jsonify({"message": "could not verify code, please contact admin"}), 500)




@users_blueprint.route("/users/info", methods=['GET'])
def user_info():
    """ view user info ,
        required headers fields:
        "email":"<email here>",
        "verification_id":"<>verification_id here"

        returned:
        {
            "current_balance": "5",
            "email": "k4@k.com",
            "is_verfied": "True",
            "mobile": "<mobile number...>"
        }
    """
    email = request.headers.get('email')
    verification_id = request.headers.get('verification_id')
    if not (email and verification_id):
        return make_response(jsonify({'message': 'headers are missing email and/or verification_id'}), 403)

    user = User.select().where(User.email == email,
                               User.verification_id == verification_id).first()
    if not user:
        return make_response(jsonify({'message': 'email and/or verification_id are invalid'}), 403)
    else:
        return make_response(jsonify(user_info_schema.dump(user)), 200)


