from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...





from pathlib import Path
import subprocess









class XCmd:
    MODES = {
        "SILENT":   dict(stdout=subprocess.DEVNULL,     stderr=subprocess.DEVNULL),
        "VERBOSE":  dict(stdout=subprocess.PIPE,        stderr=subprocess.PIPE),
        "ERROR":    dict(stdout=subprocess.DEVNULL,     stderr=subprocess.PIPE),
        "LIVE":     dict(stdout=None,                   stderr=None)
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
    