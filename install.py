from pathlib import Path
import subprocess
import sys



class XCmd:
    MODES = {
        "SILENT": dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
        "VERBOSE": dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE),
        "ERROR": dict(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE),
        "LIVE": dict(stdout=None, stderr=None)
    }

    @staticmethod
    def exec(cmd:str="", cwd:str|Path=None, check:bool=True, shell:bool=True, mode="ERROR"):
        mode: dict = XCmd.MODES.get(mode, XCmd.MODES["LIVE"])
        stdout:int = mode.get("stdout", subprocess.PIPE)
        stderr:int = mode.get("stderr", subprocess.PIPE)
        return subprocess.run(cmd, shell=shell, check=check, cwd=cwd, stdout=stdout, stderr=stderr)

    @staticmethod
    def setcwd(cwd:str|Path=None, check:bool=True, shell:bool=True):
        return subprocess.run(f"cd {cwd}", shell=shell, check=check)

    @staticmethod
    def getcwd():
        return Path.cwd()
    
    
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