from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...



from pathlib import Path





class XStatsDisk:
    def __init__(self, drive:str|Path=Path("C:\\")):
        self.drive = drive

        self.init()


    def init(self):
        ...


