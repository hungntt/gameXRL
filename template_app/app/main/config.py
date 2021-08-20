"""
Configuration constants for application
"""
import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))


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
