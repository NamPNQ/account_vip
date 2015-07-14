from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column('id', db.Integer, primary_key=True)
    site = db.Column('site', db.String)
    identity = db.Column('identity', db.String)
    password = db.Column('password', db.String)