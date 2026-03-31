from pathlib import Path
import sys

from xonnel_cmd import XCmd
from xonnel_git import XGit


class Install:
    BASE = Path(r"C:\Code\Python\Packages")

    def __init__(self, filter="xonnel"):
        self.filter = filter
        self.installpip()
        self.installgit()

    def installpip(self):
        packages = []
        for d in self.BASE.iterdir():
            if d.is_dir() and d.name.startswith(self.filter):
                packages.append(d)

        n = len(packages)
        print(f"Found {n} packages to install.")

        for i, d in enumerate(packages, 1):
            print(f"[INSTALLING] [{i}/{n}] {d}")
            try:
                XCmd.exec(cmd=f"{sys.executable} -m pip install --upgrade .", cwd=d)
            except Exception as e:
                print(f"[INSTALLING] [FAILED] {e}")

    def installgit(self):
        git = XGit(path=self.BASE)
        git.post()
        git.push("committing changes")
        


if __name__ == "__main__":
    Install("xonnel")