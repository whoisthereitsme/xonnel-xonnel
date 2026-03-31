from xonnel_json import XJson


class YLogCfg:
    PATH = r"C:\Code\Python\Packages\xonnel-log\xonnel_log\ylog1\ylog.json"

    def __init__(self):
        self.config:dict = XJson.load(path=self.PATH) or {}

        self.init()

    def init(self):
        self.host: str      = self.config.get("host", None)
        self.port: int      = self.config.get("port", None)
        self.name: str      = self.config.get("name", None)
        self.poll: float    = self.config.get("poll", None)
        self.geom: str      = self.config.get("geom", None)
        self.icon: str      = self.config.get("icon", None) 
        self.done: str      = self.config.get("done", None)

        if any(x is None for x in [self.host, self.port, self.name, self.poll, self.geom, self.icon, self.done]):
            raise ValueError(f"[ERROR] YLogCfg.init() missing required config values, config={self.config}")






