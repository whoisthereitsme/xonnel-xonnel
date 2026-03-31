from .ylogcfg import YLogCfg
from .ylogsock import LogSock
from .ylogapp import LogApp
from .ylogtray import LogTray

from PIL import Image
from pathlib import Path

from xonnel_exe import XExe
from xonnel_json import XJson
from xonnel_png import XPng




class YLog:
    def __init__(self):
        self.cfg: YLogCfg = YLogCfg()

        self.icon: Path = None
        self.sock: LogSock = None
        self.app: LogApp = None
        self.tray: LogTray = None

        self.init()
        self.post()

    def init(self):
        icon: Image = XPng.new(text=self.cfg.name)
        XPng.save(path=self.cfg.icon, data=icon)

        self.icon = Path(self.cfg.icon)

        self.sock = LogSock(ylog=self)
        self.app = LogApp(ylog=self)
        self.tray = LogTray(ylog=self)

    def post(self):
        if self.cfg.done is False:
            XExe(path=Path(__file__), icon=str(self.icon))

            self.cfg.config["done"] = True
            XJson.save(path=self.cfg.PATH, data=self.cfg.config)

            self.cfg = YLogCfg()

        if self.cfg.done is True:
            self.tray.run()
            self.app.run()


if __name__ == "__main__":
    ylog = YLog()