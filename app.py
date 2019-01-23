from flask import Flask
import config
import models
import logging
from resources.users import users_blueprint
from resources.messages import messages_blueprint

logger = logging.getLogger("App/Runner")
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    models.initialize()
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Server is running a kin demo sms simple api {}".format(config.API_VERSION)

    app.register_blueprint(users_blueprint, url_prefix=config.URL_PREFIX)
    app.register_blueprint(messages_blueprint, url_prefix=config.URL_PREFIX)
    logger.info("About to run kin demo server...")
    app.run(debug=config.DEBUG,port=config.PORT,host=config.HOST)
