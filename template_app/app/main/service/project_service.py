"""
Healcheck service
"""
from . import *

from ..model.project_model import Project
from ..model.domain_model import Domain

from flask import render_template, Response


class ProjectService(object):
    """
    Demo service methods
    """
    @staticmethod
    def home():
        """
        Render home page
        """

        projects = Project.query.all()
        for p in projects:

            project_type = Domain.query.filter(Domain.Id==p.DomainId).first()
            if project_type:
                p.domain = project_type.Type
            else:
                p.domain = ""

        return Response(render_template("index.html", projects=projects),
                            mimetype='text/html')
