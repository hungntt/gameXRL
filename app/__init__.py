"""
Initialize api
"""
import os

from flask import Flask

TEMPLATE_DIR = os.path.abspath('../templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
