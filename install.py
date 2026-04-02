from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import time
import sys
from pathlib import Path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import time
import sys
import subprocess
from pathlib import Path







class InstallStandalone:
    BASE = Path(r"C:\Code\Python\Packages")

    def __init__(self, filter="xonnel"):
        self.filter = filter
        self.installpmodules()
        self.committogithub()

    def run(self, cmd: str | list[str] = "", cwd: str | Path = None, check: bool = True, shell: bool = True, mode: str = "ERROR"):
        modes = {
            "SILENT":  dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
            "VERBOSE": dict(stdout=subprocess.PIPE,    stderr=subprocess.PIPE),
            "ERROR":   dict(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE),
            "LIVE":    dict(stdout=None,               stderr=None),
        }

        modecfg = modes.get(mode, modes["LIVE"])
        stdout = modecfg.get("stdout", subprocess.PIPE)
        stderr = modecfg.get("stderr", subprocess.PIPE)

        return subprocess.run(
            cmd,
            shell=shell,
            check=check,
            cwd=str(cwd) if cwd is not None else None,
            stdout=stdout,
            stderr=stderr,
            text=True,
        )

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
            if "xonnel-xonnel" in d.name:       # skip installing the collection package and install it in the end since it is the collection of all the other packages
                xonxon = d
            else:
                self.installmodule(path=d, id=i, total=n)

        if xonxon:
            self.installmodule(path=xonxon, id=n, total=n)

        t1 = time.time()
        print(f"[INFO] [Install.installpmodules()] [Finished installing packages in {t1 - t0:.2f} seconds!]")

    def installmodule(self, path: str | Path = None, id: int = None, total: int = None):
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
            self.run(
                cmd=[sys.executable, "-m", "pip", "install", "--upgrade", "."],
                cwd=path,
                shell=False,
                mode="SILENT",
            )
            t1 = time.time()
            print(f"[SUCCESS] [Install.installmodule()] [Successfully installed module: {path.name} in {t1 - t0:.2f} seconds]")

        except Exception as e:
            print(f"[ERROR] [Install.installmodule()] [Failed to install module: {e}]")

    def committogithub(self):
        t0 = time.time()
        print("[INFO] [Install.committogithub()] [Committing changes to GitHub...]")

        try:
            name = "whoisthereitsme"
            repo = "xonnel-xonnel"
            branch = "main"
            link = f"https://github.com/{name}/{repo}.git"

            self.run("git --version", cwd=self.BASE, mode="ERROR")
            self.run("git init", cwd=self.BASE, mode="ERROR")
            self.run(f"git branch -M {branch}", cwd=self.BASE, mode="ERROR")

            try:
                self.run("git remote get-url origin", cwd=self.BASE, mode="SILENT")
                self.run(f"git remote set-url origin {link}", cwd=self.BASE, mode="ERROR")
            except:
                self.run(f"git remote add origin {link}", cwd=self.BASE, mode="ERROR")

            self.run("git add .", cwd=self.BASE, mode="ERROR")

            try:
                self.run('git commit -m "committing changes"', cwd=self.BASE, mode="ERROR")
            except:
                print("[INFO] [Install.committogithub()] [No changes to commit]")

            self.run(f"git push origin {branch}", cwd=self.BASE, mode="ERROR")

            t1 = time.time()
            print(f"[INFO] [Install.committogithub()] [Installation complete and changes committed to GitHub in {t1 - t0:.2f} seconds!]")

        except Exception as e:
            print(f"[ERROR] [Install.committogithub()] [Failed to commit changes to GitHub: {e}]")

























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
    filter = "xonnel-xonnel"
    for i in range(1):    
        try:
            from xonnel_git import XGit
            from xonnel_cmd import XCmd
            Install(filter=filter)
        except ImportError as e:
            print("using fallback InstallStandalone since some modules are not installed yet.")
            InstallStandalone(filter=filter)








