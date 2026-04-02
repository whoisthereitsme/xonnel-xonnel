from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path
import shutil







class XDelete:
    def __init__(self, path:str|Path=None):
        if path is None:
            raise ValueError("[ERROR] XDelete.__init__() path cannot be None")

        path = Path(path)
        if path.exists():
            if path.is_file():       self._deletefile(path)
            if path.is_dir():        self._deletedir(path)
        else:
            raise ValueError(f"[ERROR] XDelete.__init__() Source does not exist: {path}")

    def _deletefile(self, path:Path):
        if path.exists() and path.is_file():
            path.unlink()

    def _deletedir(self, path:Path):
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
