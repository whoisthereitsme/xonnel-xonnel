from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path


from xonnel_copy import XCopy



class XDotType:
    @classmethod
    def copy(cls, src:str|Path=None, tgt:str|Path=None):
        XCopy(src=src, tgt=tgt)
    
    @classmethod
    def move(cls, src:str|Path=None, tgt:str|Path=None):
        ... # same per filetype implementation here!
    
    @classmethod
    def delete(cls, path:str|Path=None):
        ... # same per filetype implementation here!

    @classmethod
    def ensure(cls, path:str|Path=None):
        ... # same per filetype implementation here!

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
