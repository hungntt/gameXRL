'''
Initialize api
'''
from flask_restplus import Api
from flask import Blueprint

from .main.controller.project_controller import api as pr_ct
from .main.controller.healthcheck_controller import api as hc_ct


blueprint = Blueprint('api', __name__, template_folder='templates', static_url_path='', static_folder='static')


api = Api(blueprint,
          title='FLASK RESTPLUS API',
          version='1.0',
          description='flask restplus web service'
          )


api.add_namespace(pr_ct, path='/projects')
api.add_namespace(hc_ct, path='/healthcheck')
