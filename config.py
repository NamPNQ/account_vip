import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'account_vip.db')