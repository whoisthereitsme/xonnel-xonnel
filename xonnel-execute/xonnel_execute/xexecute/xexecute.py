from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import sys





from pathlib import Path
from xonnel_cmd import XCmd







class XExecute:
    def __new__(cls, path:str|Path=None, args:list[str]=None, cwd:str|Path=None, check:bool=True, mode:str="ERROR"):
        if path is None:
            raise ValueError("[ERROR] XExecute.__new__() path cannot be None")

        path = Path(path)
        if not path.exists():
            raise ValueError(f"[ERROR] XExecute.__new__() Source does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"[ERROR] XExecute.__new__() Source must be a file: {path}")

        return cls._exec(path=path, args=args, cwd=cwd, check=check, mode=mode)

    @classmethod
    def _exec(cls, path:Path=None, args:list[str]=None, cwd:str|Path=None, check:bool=True, mode:str="ERROR"):
        args = args or []
        ext = path.suffix.lower()
        cmd = None
        if ext == ".exe":
            cmd = [str(path), *args]
        elif ext in (".bat", ".cmd"):
            cmd = ["cmd", "/c", str(path), *args]
        elif ext == ".ps1":
            cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(path), *args]
        elif ext == ".py":
            cmd = [sys.executable, str(path), *args]
        elif ext == ".sh":
            cmd = ["bash", str(path), *args]

        if cmd is not None:
            return XCmd.exec(cmd=cmd, cwd=cwd, check=check, shell=False, mode=mode)
        raise ValueError(f"[ERROR] XExecute._exec() Unsupported file type: {ext}")
        