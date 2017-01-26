__author__ = 'mithunmohan'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_redis import FlaskRedis
#from tests.redis_mock import mock_redis_client, MockRedis

from mockredis import MockRedis


from sqlalchemy import create_engine
"""
app = Flask(__name__)
app.debug = True
app.config.from_object('config')
"""
#db.init_app(app)
#db = SQLAlchemy()
#redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
def create_app(test=None):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object('config')
    from model import db
    db.init_app(app)
    #from model import redis_con
    if test is not None:
        print "here"
        app.redis_con = FlaskRedis.from_custom_provider(MockRedis)
        app.redis_con.init_app(app)
    else:
        print "false"
        app.redis_con = FlaskRedis(app)
        app.redis_con.init_app(app)
    from app.views import mmmm
    app.register_blueprint(mmmm)
    return app


"""
app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

def create_app():
    redis_con.init_app(app)
    return app

def createRedis():
    if app.config["TESTING"] == True:
        print "????????"
        redis_con = mock_redis_client()
    else:
        print "!!!!!!!!"
        redis_con = FlaskRedis(app)
    return redis_con
#redis_con = redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
#redis_con = redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
from app import views, model
"""
