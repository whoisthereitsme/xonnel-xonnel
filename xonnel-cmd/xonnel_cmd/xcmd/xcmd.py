from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...










from pathlib import Path
import subprocess












class XCmd:
    MODES = {
        "SILENT":   dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
        "VERBOSE":  dict(stdout=subprocess.PIPE,    stderr=subprocess.PIPE),
        "ERROR":    dict(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE),
        "LIVE":     dict(stdout=None,               stderr=None),
    }

    @staticmethod
    def exec(cmd:str|list[str]="", cwd:str|Path=None, check:bool=True, shell:bool=True, mode:str="ERROR"):
        mode = XCmd.MODES.get(mode, XCmd.MODES["LIVE"])
        stdout = mode.get("stdout", subprocess.PIPE)
        stderr = mode.get("stderr", subprocess.PIPE)

        return subprocess.run(
            cmd,
            shell=shell,
            check=check,
            cwd=str(cwd) if cwd is not None else None,
            stdout=stdout,
            stderr=stderr,
            text=True,
        )

    @staticmethod
    def setcwd(cwd:str|Path=None, check:bool=True, shell:bool=True):
        return subprocess.run(f'cd /d "{cwd}"', shell=shell, check=check)

    @staticmethod
    def getcwd():
        return Path.cwd()