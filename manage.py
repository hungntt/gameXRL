"""
Create Flask app, manage API run or test
"""
import os
import unittest
from flask_script import Manager
from app import blueprint
from app.main import db, create_app


app = create_app(os.getenv("PROJ_CODE") or "dev")
db.create_all(app=app)
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)


@manager.command
def run():
    """Use python manage.py run to run main application"""
    app.run(use_reloader=False)


@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
