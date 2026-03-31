from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import subprocess
from pathlib import Path


class XCmd:
    @staticmethod
    def exec(cmd: str = "", cwd: str | Path = None, check: bool = True):
        print(f"[EXEC] {cmd} (CWD: {cwd})")
        return subprocess.run(cmd, shell=True, check=check, cwd=cwd)


class XGit:
    def __init__(
        self,
        name: str = "whoisthereitsme",
        repo: str = "xonnel-xonnel",
        branch: str = "main",
        path: str | Path = None,
    ):
        self.name = name
        self.repo = repo
        self.branch = branch
        self.path = Path(path) if path else None

        self.init()

    def init(self):
        if not self.path:
            raise ValueError("path cannot be None")

        self.link = f"https://github.com/{self.name}/{self.repo}.git"
        XCmd.exec("git --version")

    def post(self):
        XCmd.exec("git init", cwd=self.path)
        XCmd.exec(f"git branch -M {self.branch}", cwd=self.path)

        try:
            XCmd.exec("git remote get-url origin", cwd=self.path)
            XCmd.exec(f"git remote set-url origin {self.link}", cwd=self.path)
        except subprocess.CalledProcessError:
            XCmd.exec(f"git remote add origin {self.link}", cwd=self.path)

    def push(self, msg: str = "update"):
        XCmd.exec("git add .", cwd=self.path)

        try:
            XCmd.exec(f'git commit -m "{msg}"', cwd=self.path)
        except subprocess.CalledProcessError:
            print("[INFO] no changes to commit")

        XCmd.exec(f"git push origin {self.branch}", cwd=self.path)

    def pull(self):
        XCmd.exec(f"git pull origin {self.branch}", cwd=self.path)


def test():
    git = XGit(path=r"C:\Code\Python\Packages")
    git.post()
    git.push("committing changes")


if __name__ == "__main__":
    test()