"""
Create API
"""

from flask_restplus import Resource
from ..service.project_service import ProjectService
from flask_restplus import Namespace


api = Namespace('projects')


@api.route("")
class Project(Resource):
    """Home web page"""
    @api.doc('Home Page')
    def get(self):
        return ProjectService.home()
