
import os
from tests.redis_mock import mock_redis_client
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_URL = "redis://localhost:6379/0"
REDIS_LOCAL = mock_redis_client()