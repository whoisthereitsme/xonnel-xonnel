from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...





import ctypes
import shutil
from pathlib import Path





from xonnel_stats_data import XStatsData






class XStatsDisk:
    def __init__(self, path:str|Path=None, freq:float=1.0):
        self.path = Path(path) if path else None
        self.freq = freq

        self.init()

    def init(self):
        self.size = XStatsData(unit="GiB")
        self.used = XStatsData(unit="GiB")
        self.free = XStatsData(unit="GiB")
        self.perc = XStatsData(unit="%")

    def _GiB(self, bytes: int):
        return bytes / (1024 ** 3)

    def _per(self, val: float, max: float):
        if max == 0:
            return 0.0
        return (val / max) * 100.0

    def getsize(self):
        return self._GiB(shutil.disk_usage(self.path).total)

    def getused(self):
        return self._GiB(shutil.disk_usage(self.path).used)

    def getfree(self):
        return self._GiB(shutil.disk_usage(self.path).free)

    def getperc(self):
        return self._per(self.getused(), self.getsize())

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        self.size.append(data=self.getsize())
        self.used.append(data=self.getused())
        self.free.append(data=self.getfree())
        self.perc.append(data=self.getperc())

    def update_data(self):
        self.size.update()
        self.used.update()
        self.free.update()
        self.perc.update()




class XStatsDisks:
    def __init__(self, drives: list[str] | None = None):
        self.drives = drives
        self.init()

    def init(self):
        self.disks: dict[str, XStatsDisk] = {}

        drives = self.drives if self.drives is not None else self.getdrives()

        for drive in drives:
            disk = self.newdisk(path=f"{drive}:/")
            if disk:
                self.disks[drive] = disk
                setattr(self, drive, disk)

    @classmethod
    def getdrives(cls) -> list[str]:
        drives = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                drives.append(chr(65 + i))  # 65 = "A"
        return drives

    def newdisk(self, path:str|Path=None):
        if not path:
            return None

        path = Path(path)

        if not path.exists():
            print(f"[WARN] [XStatsDisks.newdisk()] [Path does not exist: {path}]")
            return None

        try:
            disk: XStatsDisk = XStatsDisk(path=path)
            self.disks[path.drive.replace(":", "")] = disk
            return disk
        except Exception as e:
            print(f"[WARN] [XStatsDisks.newdisk()] [Failed to create disk for {path}: {e}]")
            return None

    def update(self):
        for disk in self.disks.values():
            disk.update()


if __name__ == "__main__":
    disks = XStatsDisks()
    print(disks.getdrives())
    print(disks.disks)

    disks.update()

    if "C" in disks.disks:
        print(disks.disks["C"].getsize())
        print(disks.disks["C"].getused())
        print(disks.disks["C"].getfree())
        print(disks.disks["C"].getperc())