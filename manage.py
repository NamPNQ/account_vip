from flask.ext.script import Manager
from app import app
from models import db

manager = Manager(app)


@manager.command
def createdb():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    manager.run()