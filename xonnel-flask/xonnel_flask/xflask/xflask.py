from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




import flask
from xflaskview import XFlaskView













class XFlask:
    View:XFlaskView = XFlaskView
    Show = flask.render_template

    def __init__(self):
        self.init()
        

    def init(self):
        self.app = flask.Flask(__name__)

    def run(self, host="127.0.0.1", port=5000, debug=True, *args, **kwargs):
        self.app.run(host=host, port=port, debug=debug, *args, **kwargs)

    def _methods(self, view:XFlaskView=None):
        return [method.upper() for method in ["get", "post", "put", "delete", "patch", "options", "head"] if hasattr(view, method)]

    def rule(self, route:str="/", view:XFlaskView=None):
        methods = self._methods(view=view)
        self.app.add_url_rule(route, view.__name__, view.as_view(view.__name__), methods=methods)





