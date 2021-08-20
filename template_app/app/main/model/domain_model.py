"""
Module for domains table mapping.
"""

from . import *


class Domain(db.Model):
    """
    Mapping to table 'domains' in database.
    """
    __tablename__ = "domains"
    Id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(255))

    def __repr__(self) -> str:
        return "<Domain %r>" % self.Type

    def get_all(self):
        pass
