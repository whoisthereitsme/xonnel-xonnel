from pathlib import Path
import shutil
import subprocess
import sys

from xonnel_png import XPng


class XExe:
    DIST = Path(r"C:\Code\.dist")
    TEMP = Path(r"C:\Code\.temp")

    def __init__(self, path:str|Path=None, icon:str|Path=None):
        self.path = Path(path) if path else None
        self.icon = Path(icon) if icon else None
        self.default_icon = None

        self.init()
        self.post()

    def init(self):
        if not self.path:
            print("[ERROR] [XExe] path=None")
            self.ok = False
            return

        if not self.path.exists() or self.path.suffix.lower() != ".py":
            print(f"[ERROR] [XExe] invalid path: {self.path}")
            self.ok = False
            return

        self.path = self.path.resolve()
        self.name = self.path.stem
        self.base = self.path.parent
        self.dist = self.DIST
        self.build = self.TEMP / self.name
        self.spec = self.build / f"{self.name}.spec"
        self.exe = self.dist / f"{self.name}.exe"
        self.default_icon = self.build / "__xexe_icon.png"

        self.dist.mkdir(parents=True, exist_ok=True)
        self.build.mkdir(parents=True, exist_ok=True)

        if not self.icon:
            self.icon = self.default_icon
            img = XPng.new(size=(256, 256), color=(0, 0, 0, 255), text=self.name[:2].upper())
            if not img or not XPng.save(self.icon, img):
                print("[ERROR] [XExe] icon create failed")
                self.ok = False
                return
        else:
            self.icon = self.icon.resolve()
            if not self.icon.exists():
                print(f"[ERROR] [XExe] icon not found: {self.icon}")
                self.ok = False
                return

        self.ok = True

    def post(self):
        if self.ok and self.run():
            self.clean()

    def run(self):
        try:
            subprocess.run(
                [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile",
                    "--noconfirm",
                    "--clean",
                    "--name", self.name,
                    "--distpath", str(self.dist),
                    "--workpath", str(self.build / "build"),
                    "--specpath", str(self.build),
                    "--icon", str(self.icon),
                    str(self.path),
                ],
                cwd=self.base,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

            if not self.exe.exists():
                print(f"[ERROR] [XExe] exe not created: {self.exe}")
                return False

            print(f"[XExe] {self.exe}")
            return True

        except Exception as e:
            print(f"[ERROR] [XExe.run] {e}")
            return False

    def clean(self):
        try:
            if self.build.exists():
                shutil.rmtree(self.build, ignore_errors=True)
            return True
        except Exception as e:
            print(f"[ERROR] [XExe.clean] {e}")
            return False

    def __repr__(self):
        return f"<XExe path={self.path} ok={self.ok}>"
    





