__author__ = 'mithunmohan'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_redis import FlaskRedis

from tests.redis_mock import mock_redis_client



app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
redis_con = FlaskRedis(app)
#redis_con = redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
#redis_con = redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)

from app import views, model
