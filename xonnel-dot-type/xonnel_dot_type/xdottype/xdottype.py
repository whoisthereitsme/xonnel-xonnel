from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path






from xonnel_copy import XCopy
from xonnel_move import XMove
from xonnel_delete import XDelete
from xonnel_ensure import XEnsure
from xonnel_pack import XPack








class XDotType:
    """
    SHARED METHODS FOR ALL EXTENSIONS!
    """
    @classmethod
    def copy(cls, src:str|Path=None, tgt:str|Path=None):
        XCopy(src=src, tgt=tgt)
    
    @classmethod
    def move(cls, src:str|Path=None, tgt:str|Path=None):
        XMove(src=src, tgt=tgt)
    
    @classmethod
    def delete(cls, path:str|Path=None):
        XDelete(path=path)

    @classmethod
    def ensure(cls, path:str|Path=None):
        XEnsure(path=path)

    @classmethod
    def pack(cls, src:str|Path=None, tgt:str|Path=None):
        XPack(src=src, tgt=tgt)
    




    """
    METHODS TO BE OVERRIDDEN BY EACH EXTENSION!
    - if an extension does not support a method, it should raise NotImplementedError
    - if an extension supports a method, it should override it and implement the functionality
    """
    @classmethod
    def load(cls, path:str|Path=None):
        raise NotImplementedError(f"XDotType.load() is not supported for {path.suffix}")

    @classmethod
    def save(cls, path:str|Path=None, data=None):
        raise NotImplementedError(f"XDotType.save() is not supported for {path.suffix}")

    
    @classmethod
    def unpack(cls, path:str|Path=None):
        raise NotImplementedError(f"XDotType.unpack() is not supported for {path.suffix}")

    @classmethod
    def run(cls, path:str|Path=None):
        raise NotImplementedError(f"XDotType.run() is not supported for {path.suffix}")
