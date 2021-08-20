"""
Module for projects table mapping.
"""

from . import *


class Project(db.Model):
    """
    Mapping to table 'projects' in database.
    """
    __tablename__ = "projects"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    DomainId = db.Column(db.String(255), db.ForeignKey("domains.Id"))

    def __repr__(self) -> str:
        return "<Project %r>" % self.Name

    def get_all(self):
        pass
