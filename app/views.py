import json
#from run import app
from app.model import *
from flask import request
from flask import abort
from flask_httpauth import HTTPBasicAuth
#from app import redis_con
import re
from utility.apioutput import APIOutput

auth = HTTPBasicAuth()

from flask import current_app, Blueprint

mmmm = Blueprint('mmmm', __name__)

@auth.verify_password
def verify_pw(username, auth_id):
    accnt = Account.query.filter_by(username = username).first()
    if not accnt:
        return False
    elif accnt:
        if accnt.auth_id == auth_id:
            return True
        else:
            return False
    return True


@mmmm.route('/')
def show():
    return "Das"


@mmmm.route('/inbound/sms',methods=['POST'])
@auth.login_required
def inbound():
    if request.method != "POST":
        abort(405)
    outputapi = APIOutput()
    try:
        rr = json.loads(request.data)
        checkParam(rr)
        checkValid(rr)
        to_param = rr["to"]
        from_param = rr["from"]
        text_param = rr["text"]

        account_id = Account.query.filter_by(username = auth.username()).first().id
        phnum = PhoneNumber.query.filter_by(account_id = account_id).first().number
        if phnum != to_param:
            outputapi.setError("to parameter not found")
        else:
            if re.match("STOP[\r\n]", text_param) is not None:
                current_app.redis_con.set(from_param+"-"+to_param,"STOP")
                current_app.redis_con.expire(from_param+"-"+to_param,4*3600)
            outputapi.setMessage("inbound sms ok")
        return outputapi.printJSONOutout()
    except ParamMissingException as e:
        outputapi.setError(e.message)
        return outputapi.printJSONOutout()
    except ParamInValidException as e:
        outputapi.setError(e.message)
        return outputapi.printJSONOutout()
    except:
        outputapi.setError("unknown failure")
        return outputapi.printJSONOutout()


@mmmm.route('/outbound/sms', methods=['POST'])
@auth.login_required
def outbound():
    if request.method != "POST":
        abort(405)
    outputapi = APIOutput()
    try:
        print request.data
        rr = json.loads(request.data)
        #check if the params are present
        checkParam(rr)
        checkValid(rr)
        to_param = rr["to"]
        from_param = rr["from"]
        text_param = rr["text"]
        if current_app.redis_con.get(from_param) is None:
            current_app.redis_con.set(from_param,1)
            current_app.redis_con.expire(from_param, 30)
        else:
            requ_cnt = int(current_app.redis_con.get(from_param))
            if (requ_cnt < 5 ):
                current_app.redis_con.incr(from_param)
            else:
                outputapi.setError("limit reached for from " + from_param)
                return outputapi.printJSONOutout()
        if current_app.redis_con.get(from_param+"-"+to_param) == "STOP":
            outputapi.setError("sms from " +from_param  +  "  to "+ to_param+  " blocked by STOP request")
            return outputapi.printJSONOutout()

        account_id = Account.query.filter_by(username = auth.username()).first().id
        phnum = PhoneNumber.query.filter_by(account_id = account_id).first().number
        if phnum != from_param:
            outputapi.setError("from parameter not found")
        else:
            outputapi.setMessage("outbound sms ok")

        return outputapi.printJSONOutout()
    except ParamMissingException as e:
        outputapi.setError(e.message)
        return outputapi.printJSONOutout()
    except ParamInValidException as e:
        outputapi.setError(e.message)
        return outputapi.printJSONOutout()
    except:
        outputapi.setError("unknown failure")
        return outputapi.printJSONOutout()


