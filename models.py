import datetime
from peewee import *
from argon2 import PasswordHasher


DATABASE = SqliteDatabase('kin.sqlite')
HASHER = PasswordHasher()


class Plan(Model):
    title = CharField()
    initial_balance = DecimalField(default=25.0)
    message_cost = DecimalField(default=10.0)

    class Meta:
        database = DATABASE


class User(Model):
    email = CharField(unique=True)
    mobile = CharField()
    is_verfied = BooleanField(default=False)
    verification_id = CharField()
    password = CharField()
    current_balance = DecimalField()
    plan = ForeignKeyField(Plan, related_name='plan')
    
    class Meta:
        database = DATABASE

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        try:
            HASHER.verify(self.password, password)
            return True
        except Exception as err:
            return False





class Message(Model):
    user = ForeignKeyField(User, related_name='messages')
    message = TextField(default='')
    to = TextField(default='')
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE





def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Message, Plan], safe=True)
    DATABASE.close()
