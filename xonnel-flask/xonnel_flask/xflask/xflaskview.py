



import base64


from flask.views import MethodView
from flask import jsonify
from datetime import datetime



class XFlaskView(MethodView):
    def _encode(self, data:bytes):
        return base64.b64encode(data).decode("utf-8")
    
    def _decode(self, data:str):
        return base64.b64decode(data.encode("utf-8"))
    
    def _data(self, msg:str="", **kwargs):
        resp = {}
        resp["message"] = msg
        resp["date"] = datetime.now().strftime("%Y-%m-%d")
        resp["time"] = datetime.now().strftime("%H:%M:%S")

        if kwargs.get("data", None) is not None:
            resp["data"] = self._encode(kwargs["data"])
        
        resp.update(kwargs)

        return jsonify(resp)
    
    def _501(self, msg:str="", **kwargs):
        return self._data(msg=msg, **kwargs), 501
    
    def _200(self, msg:str="", **kwargs):
        return self._data(msg=msg, **kwargs), 200
    

    def get(self):
        return self._501(msg="GET method not implemented")
    
    def post(self):
        return self._501(msg="POST method not implemented")
    
    def put(self):
        return self._501(msg="PUT method not implemented")
    
    def delete(self):
        return self._501(msg="DELETE method not implemented")
    
    def patch(self):
        return self._501(msg="PATCH method not implemented")
    
    def options(self):
        return self._501(msg="OPTIONS method not implemented")
    
    def head(self):
        return self._501(msg="HEAD method not implemented")

