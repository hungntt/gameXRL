"""
Initialize logger for logging
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from ..config import Config
import os


basedir = os.path.abspath(os.path.dirname(__file__))
log_folder = os.path.join(basedir, '../log')
if not os.path.exists(log_folder):
    os.mkdir(log_folder)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


logname = os.path.join(log_folder, Config.LOG_NAME)
handler = TimedRotatingFileHandler(logname, when='midnight')
handler.setLevel(logging.INFO)
type_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(type_format)


logger.addHandler(handler)
