import requests
import json

username = "plivo1"
password = "20S0KPNOIM"

url = "http://localhost:5000"
testdata = json.loads(open('testcases.json').read())
for i in testdata["testcase"]:
    print i
    resp = requests.post(url + "/outbound/sms", json=i, auth=(username, password))
    print resp.json()