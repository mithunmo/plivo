import os
import unittest
from config import basedir
from app import create_app
from app.model import PhoneNumber
from app.model import Account
from app.model import db
from app.model import checkValid
from app.model import checkParam, ParamInValidException, ParamMissingException

#from app import db
#from redis_mock import mock_redis_client, MockRedis
from mockredis import MockRedis
from flask_redis import FlaskRedis
import json
import base64
from werkzeug.datastructures import Headers
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class MockRedisWrapper(MockRedis):
    '''A wrapper to add the `from_url` classmethod'''
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()

class TestCase(unittest.TestCase):
    def setUp(self):
        """
        app.config['TESTING'] = True
        print "starting test"
        app.config['WTF_CSRF_ENABLED'] = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/mithun'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        #app.config["REDIS_HOST"] = 'localhost'
        #app.config["PORT"] = 6379
        redis_con = mock_redis_client()
        #print redis_con.get("Sdd")
        """
        #db.init_app(app)
        #db = SQLAlchemy()


        #app = create_app()
        #self.app = app.test_client()

        #redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)
        #app.config.from_object('config')
        #redis_con = mock_redis_client()
        app = create_app("dss")
        redis_con = FlaskRedis.from_custom_provider(MockRedis)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test12.db'
        #app.config['REDIS_URL'] = ""
        app.config["TESTING"] = True
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            accnt1 = Account("p@ssword","mithun",)
            db.session.add(accnt1)
            db.session.commit()

            phnum = PhoneNumber("9886297837",accnt1.id)
            db.session.add(phnum)
            db.session.commit()

            phnum1 = PhoneNumber("7022620605",accnt1.id)
            db.session.add(phnum1)
            db.session.commit()


        """
        db.init_app(app)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        with app.app_context():
            self.app = app.test_client()
            db.drop_all()
            db.create_all()

            accnt1 = Account("p@ssword","mithun",)
            db.session.add(accnt1)
            db.session.commit()

            phnum = PhoneNumber("9886297837",accnt1.id)
            db.session.add(phnum)
            db.session.commit()

            phnum1 = PhoneNumber("7022620605",accnt1.id)
            db.session.add(phnum1)
            db.session.commit()
        """
    def tearDown(self):
        pass
        #with self.app.app_context():
        #    db.drop_all()
        #PhoneNumber.query.filter_by(accountid=Account.query.filter_by(username="mithun"))
        #Account.query.filter_by(username="mithun").delete()
        #db.session.commit()
        #db.session.remove()
        #db.drop_all()


    def test_params(self):
        testparam = {"to":"9886297837","from":"9886297837","text":"hello"}
        r = checkParam(testparam)
        assert r == True

    def test_params_missing(self):
        testparam = {"from":"9886297837","text":"hello"}
        self.assertRaises(ParamMissingException, checkParam, testparam)

    def test_params_invalid(self):
        testparam = {"to":"11","from":"9886297837","text":"hello"}
        self.assertRaises(ParamInValidException, checkValid, testparam)

    def test_outbound(self):
        h = Headers()
        h.add('Authorization', 'Basic ' + base64.b64encode('mithun:p@ssword'))
        payload = {"to":"9886297837","from":"9886297837","text":"hello"}
        r = self.app.post('/outbound/sms',data=json.dumps(payload),content_type='application/json',headers=h)
        print r.data
        r= json.loads(r.data)
        assert r["message"] == "outbound sms ok"

    def test_outbound_invalid(self):
        h = Headers()
        h.add('Authorization', 'Basic ' + base64.b64encode('mithun:p@ssword'))
        payload = {"to":"9886297837","text":"hello"}
        r = self.app.post('/outbound/sms',data=json.dumps(payload),content_type='application/json',headers=h)
        r= json.loads(r.data)
        assert r["error"] == "from is missing"


    def test_inbound(self):
        h = Headers()
        h.add('Authorization', 'Basic ' + base64.b64encode('mithun:p@ssword'))
        payload = {"to":"9886297837","from":"9886297837","text":"hello"}
        r = self.app.post('/inbound/sms',data=json.dumps(payload),content_type='application/json',headers=h)
        print r.data
        r= json.loads(r.data)
        assert r["message"] == "inbound sms ok"


if __name__ == '__main__':
    unittest.main()