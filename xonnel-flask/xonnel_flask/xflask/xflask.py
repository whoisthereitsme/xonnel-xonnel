from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




import flask
from xflaskview import XFlaskView













class XFlask:
    def __init__(self):
        self.init()
        

    def init(self):
        self.app = flask.Flask(__name__)

    def _methods(self, view:XFlaskView=None):
        return [method.upper() for method in ["get", "post", "put", "delete", "patch", "options", "head"] if hasattr(view, method)]

    def rule(self, route:str="/", view:XFlaskView=None):
        methods = self._methods(view=view)
        self.app.add_url_rule(route, view.__name__, view.as_view(view.__name__), methods=methods)





