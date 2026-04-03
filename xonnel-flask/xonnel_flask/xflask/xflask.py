from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




import flask



class XFlask:
    METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]

    def __init__(self):
        self.init()
        

    def init(self):
        self.app = flask.Flask(__name__)

    def _methods(self, methods:list):
        for method in methods:
            if method not in self.METHODS:
                raise ValueError(f"Invalid HTTP method: {method}")

    def rule(self, route:str="/", callback:callable=None, methods=["GET"]):
        self._methods(methods)
        self.app.add_url_rule(route, callback.__name__, callback, methods=methods)

