







from flask.views import MethodView
from flask import jsonify
from datetime import datetime




from xonnel_codex import XCodex






class XFlaskView(MethodView):
    def _response(self, msg:str="", **kwargs):
        resp = {}
        resp["message"] = msg
        resp["date"] = datetime.now().strftime("%Y-%m-%d")
        resp["time"] = datetime.now().strftime("%H:%M:%S")

        if kwargs.get("data", None) is not None:
            mode = kwargs.get("mode", "zlib base64")
            resp["data"] = XCodex.encode(data=kwargs["data"], mode=mode)
            resp["mode"] = mode
            kwargs.pop("data", None)
            kwargs.pop("mode", None)
        
        resp.update(kwargs)

        return jsonify(resp)
    

    
    def _100(self, msg:str="", code:int=100, **kwargs):
        return self._response(msg="[INFO] " + msg, **kwargs), code
    
    def _200(self, msg:str="", code:int=200, **kwargs):
        return self._response(msg="[OK] " + msg, **kwargs), code
    
    def _300(self, msg:str="", code:int=300, **kwargs):
        return self._response(msg="[REDIRECT] " + msg, **kwargs), code
    
    def _400(self, msg:str="", code:int=400, **kwargs):
        return self._response(msg="[ERROR CLIENT] " + msg, **kwargs), code
    
    def _500(self, msg:str="", code:int=500, **kwargs):
        return self._response(msg="[ERROR SERVER] " + msg, **kwargs), code
    


    def response(self, code:int=500, msg:str="", **kwargs):
        if code >= 100 and code < 200:
            return self._100(msg=msg, code=code, **kwargs)
        elif code >= 200 and code < 300:
            return self._200(msg=msg, code=code, **kwargs)
        elif code >= 300 and code < 400:
            return self._300(msg=msg, code=code, **kwargs)
        elif code >= 400 and code < 500:
            return self._400(msg=msg, code=code, **kwargs)
        elif code >= 500 and code < 600:
            return self._500(msg=msg, code=code, **kwargs)
        else:
            return self._500(msg="Invalid status code", code=500, **kwargs)
    


    
    
    
    

    
    def get(self):
        return self.response(msg="GET method not implemented",          code=405)
    
    def post(self):
        return self.response(msg="POST method not implemented",         code=405)
    
    def put(self):
        return self.response(msg="PUT method not implemented",          code=405)
    
    def delete(self):
        return self.response(msg="DELETE method not implemented",       code=405)
    
    def patch(self):
        return self.response(msg="PATCH method not implemented",        code=405)
    
    def options(self):
        return self.response(msg="OPTIONS method not implemented",      code=405)
    
    def head(self):
        return self.response(msg="HEAD method not implemented",         code=405)

