"""
Configuration constants for application
"""
import os
import json
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the MySQL ULR for SqlAlchemy
mysql_url = "mysql://" + os.path.join(basedir, "xrl.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)


class Config(object):
    """
    Base configuration class
    """

    LOG_NAME = 'app.log'


class DevelopmentConfig(Config):
    """
    Configuration for Development environment
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configuration for Test environment
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Configuration for Production environment
    """
    DEBUG = False


config_by_name = dict(
        dev=DevelopmentConfig,
        test=TestingConfig,
        prod=ProductionConfig
)
