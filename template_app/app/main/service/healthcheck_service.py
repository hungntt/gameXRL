"""
Healcheck service
"""

import os
import json
from flask import jsonify


class HealthCheckService(object):
    """
    Healthcheck service methods
    """
    @staticmethod
    def healthcheck():
        """
        Returns OK if server go online
        """
        resp = jsonify({'success': 'OK'})
        resp.status_code = 200
        resp.headers['Content-Type'] = 'application/json'
        return resp
