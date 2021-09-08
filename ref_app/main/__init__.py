"""
Initialize Flask application
"""
import os

import datetime
from dotenv import find_dotenv, load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name
from .utils.log import logger


# Load environment variables from file .env
env_path = find_dotenv()
load_dotenv(env_path)


# Init log
date = datetime.datetime.now()
logger.info("LOGGING FOR {}".format(date.strftime("%A-%d-%B-%Y")))


# Init database
db = SQLAlchemy()


def create_app(config_name):
    """Create Flask appication on three environments
    Arguments:
        config_name {string} -- name of environments: dev, test or prod
    Returns:
        app  -- Flask app for one environment
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
    db.init_app(app)
    app.config.from_object(config_by_name[config_name])
    return app
