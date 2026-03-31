# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
import os
import sys
import atexit
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XExit:
    FUNCTIONS = []
    DONE = False
    INITED = False

    SYS_EXIT = sys.exit
    OS_EXIT = os._exit

    @classmethod
    def register(cls, call:callable=None):
        if callable(call):
            cls.FUNCTIONS.append(call)

    @classmethod
    def onexit(cls):
        if cls.DONE:
            return

        cls.DONE = True

        for fn in cls.FUNCTIONS:
            try:
                fn()
            except Exception as e:
                print(f"[ERROR] [XExit.onexit()] [{e}]")

    @classmethod
    def sys_exit(cls, code=0):
        print("sys exit")
        cls.onexit()
        cls.SYS_EXIT(code)

    @classmethod
    def os_exit(cls, code=0):
        print("os exit")
        cls.onexit()
        cls.OS_EXIT(code)

    @classmethod
    def my_exit(cls):
        print("my exit")
        cls.onexit()

    @classmethod
    def init(cls):
        if cls.INITED:
            return

        cls.INITED = True

        sys.exit = cls.sys_exit
        os._exit = cls.os_exit
        atexit.register(cls.my_exit)




# auto-init
XExit.init()
# [!] {-}



