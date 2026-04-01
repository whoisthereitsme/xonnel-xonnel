from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import time
import sys
from pathlib import Path



from xonnel_git import XGit
from xonnel_cmd import XCmd



















class Install:
    BASE = Path(r"C:\Code\Python\Packages")

    def __init__(self, filter="xonnel"):
        self.filter = filter
        self.installpmodules()
        self.committogithub()

    def installpmodules(self):
        t0 = time.time()
        print("[INFO] [Install.installpmodules()] [Installing packages...]")
        packages = []
        for d in self.BASE.iterdir():
            if d.is_dir() and d.name.startswith(self.filter):
                packages.append(d)

        n = len(packages)
        print(f"[INFO] [Install.installpmodules()] [Found {n} packages to install.]")

        xonxon = None
        for i, d in enumerate(packages, 1):
            if "xonnel-xonnel" in d.name:       # skip installing the git package and install it in the end since its the collection of all the other packages
                xonxon = d
            else:
                self.installmodule(path=d, id=i, total=n)

        if xonxon:
            self.installmodule(path=xonxon, id=n, total=n)
        t1 = time.time()
        print(f"[INFO] [Install.installpmodules()] [Finished installing packages in {t1 - t0:.2f} seconds!]")

    def installmodule(self, path:str|Path=None, id:int=None, total:int=None):
        try:
            t0 = time.time()
            if path is None:
                print("[ERROR] [Install.installmodule()] [path cannot be None]")
                return
            path = Path(path)

            if not path.exists():
                print(f"[ERROR] [Install.installmodule()] [Path does not exist: {path.name}]")
                return
            print(f"[INFO] [Install.installmodule()] [INSTALLING [{id}/{total}] {path.name}]")
            XCmd.exec(cmd=[sys.executable, "-m", "pip", "install", "--upgrade", "."], cwd=path, mode="SILENT")
            t1 = time.time()
            print(f"[SUCCESS] [Install.installmodule()] [Successfully installed module: {path.name} in {t1 - t0:.2f} seconds]")
            
        except Exception as e:
            print(f"[ERROR] [Install.installmodule()] [Failed to install module: {e}]")


    def committogithub(self):
        t0 = time.time()
        print("[INFO] [Install.committogithub()] [Committing changes to GitHub...]")
        git = XGit(path=self.BASE)
        git.post()
        git.push("committing changes")
        t1 = time.time()
        print(f"[INFO] [Install.committogithub()] [Installation complete and changes committed to GitHub in {t1 - t0:.2f} seconds!]")
        







if __name__ == "__main__":
    Install("xonnel")






