from pathlib import Path


class YLogCfg:
    DEFAULT = {
        "name": "Log",
        "host": "127.0.0.1",
        "port": 50505,
        "poll": 0.1,
        "geom": "1600x900+100+100",
        "done": True,
        "icon": r"C:\Code\.temp\icon.png",
    }

    def __init__(self):
        self.config: dict = dict(self.DEFAULT)
        
        self.init()

    def init(self):
        self.host: str = self.config["host"]
        self.port: int = self.config["port"]
        self.name: str = self.config["name"]
        self.poll: float = self.config["poll"]
        self.geom: str = self.config["geom"]
        self.icon: str = self.config["icon"]
        self.done: bool = self.config["done"]