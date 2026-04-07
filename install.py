from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import time
import sys
import subprocess
import shutil


from pathlib import Path




from xonnel_git import XGit
from xonnel_cmd import XCmd











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

    def __init__(self, filter: str = "xonnel"):
        self.filter = str(filter)
        self.installpmodules()
        self.committogithub()

    def installpmodules(self):
        t0 = time.time()
        print("[INFO] [Install.installpmodules()] [Installing packages...]")

        packages = []
        for d in self.BASE.iterdir():
            if d.is_dir() and d.name.startswith(self.filter):
                packages.append(d)

        packages.sort(key=lambda p: p.name.lower())

        n = len(packages)
        print(f"[INFO] [Install.installpmodules()] [Found {n} packages to install.]")

        xonxon = None
        current = 0

        for d in packages:
            if d.name == "xonnel-xonnel":
                xonxon = d
                continue

            current += 1
            self.installmodule(path=d, id=current, total=n)

        if xonxon is not None:
            self.installmodule(path=xonxon, id=n, total=n)

        t1 = time.time()
        print(f"[INFO] [Install.installpmodules()] [Finished installing packages in {t1 - t0:.2f} seconds!]")

    def installmodule(self, path: str | Path = None, id: int = None, total: int = None):
        t0 = time.time()

        try:
            if path is None:
                print("[ERROR] [Install.installmodule()] [path cannot be None]")
                return

            path = Path(path)

            if not path.exists():
                print(f"[ERROR] [Install.installmodule()] [Path does not exist: {path}]")
                return

            print(f"[INFO] [Install.installmodule()] [INSTALLING [{id}/{total}] {path.name}]")
            XCmd.exec(
                cmd=[sys.executable, "-m", "pip", "install", "--upgrade", "."],
                cwd=path,
                mode="SILENT",
            )

            print(f"[INFO] [Install.installmodule()] [POST-CLEAN [{id}/{total}] {path.name}]")
            self.cleanmodule(path=path)

            t1 = time.time()
            print(f"[SUCCESS] [Install.installmodule()] [Successfully installed module: {path.name} in {t1 - t0:.2f} seconds]")

        except Exception as e:
            print(f"[ERROR] [Install.installmodule()] [Failed to install module {path}: {e}]")

    def cleanmodule(self, path: str | Path = None):
        if path is None:
            print("[ERROR] [Install.cleanmodule()] [path cannot be None]")
            return

        path = Path(path)

        targets = []

        build = path / "build"
        dist = path / "dist"

        if build.exists():
            targets.append(build)

        if dist.exists():
            targets.append(dist)

        for egg in path.glob("*.egg-info"):
            if egg.exists():
                targets.append(egg)

        for pycache in path.rglob("__pycache__"):
            if pycache.exists():
                targets.append(pycache)

        for pyc in path.rglob("*.pyc"):
            if pyc.exists():
                targets.append(pyc)

        if not targets:
            print(f"[INFO] [Install.cleanmodule()] [No cleanup needed for {path.name}]")
            return

        for target in targets:
            try:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()

                print(f"[INFO] [Install.cleanmodule()] [Removed: {target}]")

            except Exception as e:
                pass

        print(f"[INFO] [Install.cleanmodule()] [Cleanup done for {path.name}]")

    def committogithub(self):
        t0 = time.time()
        print("[INFO] [Install.committogithub()] [Committing changes to GitHub...]")
        git = XGit(path=self.BASE)
        git.post()
        git.push("committing changes")
        t1 = time.time()
        print(f"[INFO] [Install.committogithub()] [Installation complete and changes committed to GitHub in {t1 - t0:.2f} seconds!]")














def main(filter:str="xonnel"):
    Install(filter=filter)
    from xonnel_backup import XBackup
    XBackup(path=Path(r"C:\Code"), mode="ZIP")





if __name__ == "__main__":
    main(filter="xonnel-backup")
    