#from app import db
from sqlalchemy.inspection import inspect
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

#redis_con = FlaskRedis()
db = SQLAlchemy()
""" Serializable mixin """
class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Account(db.Model, Serializer):
    __tablename__ = "account"
    id = db.Column(db.Integer(), primary_key=True)
    auth_id = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(30))
    #numbers = db.relationship('PhoneNumber', backref=db.backref('phnum',cascade='all'), lazy='dynamic')

    def __init__(self, auth_id=None, username=None):
        self.auth_id = auth_id
        self.username = username

    def serialize(self):
        d = Serializer.serialize(self)
        del d['auth_id']
        return d

class PhoneNumber(db.Model):
    __tablename__ = "phone_number"
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String(40), unique=True)
    #account_id = db.Column(db.Integer(), db.ForeignKey('account.id'))
    account_id = db.Column(db.Integer())

    def __init__(self, number=None, account_id=None):
        self.number = number
        self.account_id = account_id


class ParamMissingException(Exception):
    pass


class ParamInValidException(Exception):
    pass



def checkParam(requestData):
    keys = ("to","from","text")
    for i in keys:
        if i not in requestData:
            raise ParamMissingException(i + " is missing")
    return True


def checkValid(requestData):
    if len(requestData["to"]) < 6 or len(requestData["to"]) > 16:
        raise ParamInValidException("to is not valid")
        return output
    elif len(requestData["from"]) < 6 or len(requestData["from"]) > 16:
        raise ParamInValidException("from is not valid")
    elif len(requestData["text"]) < 1 or len(requestData["text"]) > 120:
        raise ParamInValidException("text is not valid")
    else:
        return True
