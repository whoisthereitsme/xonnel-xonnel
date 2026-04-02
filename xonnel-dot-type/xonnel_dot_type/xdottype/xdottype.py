from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path


from xonnel_copy import XCopy
from xonnel_move import XMove



class XDotType:
    @classmethod
    def copy(cls, src:str|Path=None, tgt:str|Path=None):
        XCopy(src=src, tgt=tgt)
    
    @classmethod
    def move(cls, src:str|Path=None, tgt:str|Path=None):
        XMove(src=src, tgt=tgt)
    
    @classmethod
    def delete(cls, path:str|Path=None):
        if path is not None:
            path = Path(path)
            if path.exists():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    for child in path.iterdir():
                        cls.delete(child)
                    path.rmdir()

    @classmethod
    def ensure(cls, path:str|Path=None):
        if path is not None:
            path = Path(path)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)

    def load(self):
        raise NotImplementedError("XDotType.load() is not implemented!")
        ... # different per filetype, so not implemented here!

    def save(self):
        raise NotImplementedError("XDotType.save() is not implemented!")
        ... # different per filetype, so not implemented here!

    def pack(self):
        raise NotImplementedError("XDotType.pack() is not implemented!")
    
    def unpack(self):
        raise NotImplementedError("XDotType.unpack() is not implemented!")

    def run(self):
        raise NotImplementedError("XDotType.run() is not implemented!")
