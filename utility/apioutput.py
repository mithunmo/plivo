import json

class APIOutput:

    def __init__(self):
        self.output = {"message":"", "error":""}

    def setMessage(self,message):
        self.output["message"] = message


    def setError(self,error):
        self.output["error"] = error

    def printJSONOutout(self):
        return json.dumps(self.output)

