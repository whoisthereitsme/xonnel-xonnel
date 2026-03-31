from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ylog import YLog

from pathlib import Path

import pystray
from PIL import Image


class LogTray:
    def __init__(self, ylog: "YLog"):
        self.ylog: YLog = ylog
        self.init()

    def init(self):
        self.app = self.ylog.app
        self.logsocket = self.ylog.sock
        self.icon = None
        self.iconpath: Path | None = Path(self.ylog.cfg.icon) if self.ylog.cfg.icon else None

    def create_image(self):
        if self.iconpath and self.iconpath.exists():
            try:
                return Image.open(self.iconpath)
            except Exception:
                pass

        return Image.new("RGB", (64, 64), (0, 0, 0))

    def on_show(self, icon, item):
        self.app.root.after(0, self.app.show)

    def on_hide(self, icon, item):
        self.app.root.after(0, self.app.hide)

    def on_quit(self, icon, item):
        def quit_all():
            try:
                self.logsocket.shutdown()
            except Exception:
                pass

            try:
                if self.icon:
                    self.icon.stop()
            except Exception:
                pass

            self.app.quit()

        self.app.root.after(0, quit_all)

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.on_show),
            pystray.MenuItem("Hide", self.on_hide),
            pystray.MenuItem("Quit", self.on_quit),
        )

        self.icon = pystray.Icon(
            self.ylog.cfg.name,
            self.create_image(),
            self.ylog.cfg.name,
            menu,
        )
        self.icon.run_detached()