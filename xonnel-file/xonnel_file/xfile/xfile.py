from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path











from xonnel_copy        import XCopy
from xonnel_move        import XMove
from xonnel_delete      import XDelete
from xonnel_ensure      import XEnsure
from xonnel_pack        import XPack
from xonnel_unpack      import XUnpack
from xonnel_load        import XLoad
from xonnel_save        import XSave
from xonnel_execute     import XExecute







class XFile:
    @classmethod
    def delete(cls, path:str|Path=None):
        XDelete(path=path)

    @classmethod
    def ensure(cls, path:str|Path=None):
        XEnsure(path=path)

    @classmethod
    def copy(cls, src:str|Path=None, tgt:str|Path=None):
        XCopy(src=src, tgt=tgt)
    
    @classmethod
    def move(cls, src:str|Path=None, tgt:str|Path=None):
        XMove(src=src, tgt=tgt)

    @classmethod
    def pack(cls, src:str|Path=None, tgt:str|Path=None):
        XPack(src=src, tgt=tgt)
    
    @classmethod
    def unpack(cls, src:str|Path=None, tgt:str|Path=None):
        XUnpack(src=src, tgt=tgt)

    @classmethod
    def load(cls, path:str|Path=None, force:str=None):
        return XLoad(path=path, force=force)

    @classmethod
    def save(cls, path:str|Path=None, data=None, force:str=None):
        return XSave(path=path, data=data, force=force)

    @classmethod
    def execute(cls, path:str|Path=None, args:list[str]=None, cwd:str|Path=None, check:bool=True, mode:str="ERROR"):
        return XExecute(path=path, args=args, cwd=cwd, check=check, mode=mode)
