from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...







from pathlib import Path
import sys


    
from xonnel_git import XGit
from xonnel_cmd import XCmd

class Install:
    BASE = Path(r"C:\Code\Python\Packages")

    def __init__(self, filter="xonnel"):
        self.filter = filter
        self.installpmodules()
        self.committogithub()

    def installpmodules(self):
        packages = []
        for d in self.BASE.iterdir():
            if d.is_dir() and d.name.startswith(self.filter):
                packages.append(d)

        n = len(packages)
        print(f"Found {n} packages to install.")

        xonxon = None
        for i, d in enumerate(packages, 1):
            if "xonnel-xonnel" in d.name:       # skip installing the git package and install it in the end since its the collection of all the other packages
                xonxon = d
            else:
                self.installmodule(path=d, id=i, total=n)

        if xonxon:
            self.installmodule(path=xonxon, id=n, total=n)

    def installmodule(self, path:str|Path=None, id:int=None, total:int=None):
        try:
            if path is None:
                print("[ERROR] [Install.installmodule()] [path cannot be None]")
                return
            path = Path(path)

            if not path.exists():
                print(f"[ERROR] [Install.installmodule()] [Path does not exist: {path}]")
                return
            print(f"[INSTALLING] [{id}/{total}] {path}")
            XCmd.exec(cmd=[sys.executable, "-m", "pip", "install", "--upgrade", "."], cwd=path, mode="LIVE")
            
        except Exception as e:
            print(f"[ERROR] [Install.installmodule()] [Failed to install module: {e}]")


    def committogithub(self):
        git = XGit(path=self.BASE)
        git.post()
        git.push("committing changes")
        


if __name__ == "__main__":
    Install("xonnel")






