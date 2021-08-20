"""
Create API
"""

from flask import request
from flask_restplus import Resource
from ..service.healthcheck_service import HealthCheckService
from flask_restplus import Namespace


api = Namespace('healthcheck')


@api.route("")
class Healthcheck(Resource):
    """Api to Healthcheck"""
    @api.doc('Healthcheck Page')
    def get(self):
        return HealthCheckService.healthcheck()
