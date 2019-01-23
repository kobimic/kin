import os

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"
API_VERSION = "v1"
URL_PREFIX = "/api/{}".format(API_VERSION)


SECRET_KEY = os.getenv("SECRET_KEY", "bnvcbnctgrfhtrryrfgdhjdfghjsdfghuiop")
NEXMO_API_KEY = os.getenv("NEXMO_API_KEY")
NEXMO_API_SECRET = os.getenv("NEXMO_API_SECRET")
VERIFICATION_CODE_LENGTH = 4
