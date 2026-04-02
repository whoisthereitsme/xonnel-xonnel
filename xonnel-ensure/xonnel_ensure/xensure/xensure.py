from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path
import shutil







class XEnsure:
    def __init__(self, path:str|Path=None):
        if path is None:
            raise ValueError("[ERROR] XEnsure.__init__() path cannot be None")

        path = Path(path)
        if not path.exists():
            if path.is_file():       self._ensurefile(path)
            if path.is_dir():        self._ensuredir(path)
        else:
            ... # already exists, do nothing

    def _ensurefile(self, path:Path):
        path.touch()

    def _ensuredir(self, path:Path):
        path.mkdir(parents=True, exist_ok=True)
