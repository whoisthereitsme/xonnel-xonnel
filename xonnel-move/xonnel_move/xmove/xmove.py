from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

from pathlib import Path
import shutil


class XMove:
    def __init__(self, src:str|Path=None, tgt:str|Path=None):
        if src is None or tgt is None:
            raise ValueError("[ERROR] XMove.__init__() src and tgt cannot be None")

        src, tgt = Path(src), Path(tgt)
        if src.exists():
            tgt.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():       self._movefile(src, tgt)
            if src.is_dir():        self._movedir(src, tgt)
        else:
            raise ValueError(f"[ERROR] XMove.__init__() Source does not exist: {src}")
        
    def _movefile(self, src:str|Path, tgt:str|Path):
        if tgt.exists() and tgt.is_dir():
            tgt = tgt / src.name
        shutil.move(src, tgt)

    def _movedir(self, src:str|Path, tgt:str|Path):
        if tgt.exists():
            shutil.rmtree(tgt)
        shutil.move(src, tgt)
