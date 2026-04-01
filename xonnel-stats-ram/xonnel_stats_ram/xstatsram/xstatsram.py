from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import psutil

from xonnel_stats_data import XStatsData


class XStatsRam:
    def __init__(self):
        self.init()

    def init(self):
        self.size: XStatsData = XStatsData(unit="GiB")
        self.used: XStatsData = XStatsData(unit="GiB")
        self.free: XStatsData = XStatsData(unit="GiB")
        self.perc: XStatsData = XStatsData(unit="%")

    def _GiB(self, bytes: int) -> float:
        return float(bytes) / (1024 ** 3)

    def getdata(self):
        return psutil.virtual_memory()

    def getsize(self) -> float:
        data = self.getdata()
        return self._GiB(data.total)

    def getused(self) -> float:
        data = self.getdata()
        return self._GiB(data.used)

    def getfree(self) -> float:
        data = self.getdata()
        return self._GiB(data.free)

    def getperc(self) -> float:
        data = self.getdata()
        return float(data.percent)

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        data = self.getdata()
        
        self.size.append(data=self._GiB(data.total))
        self.used.append(data=self._GiB(data.used))
        self.free.append(data=self._GiB(data.free))
        self.perc.append(data=float(data.percent))

    def update_data(self):
        self.size.update()
        self.used.update()
        self.free.update()
        self.perc.update()


def test():
    ram = XStatsRam()
    ram.update()

    print(f"size: {ram.size.last()}")
    print(f"used: {ram.used.last()}")
    print(f"free: {ram.free.last()}")
    print(f"perc: {ram.perc.last()}")

    print(f"size (raw): {ram.size.last(format=False)}")
    print(f"used (raw): {ram.used.last(format=False)}")
    print(f"free (raw): {ram.free.last(format=False)}")
    print(f"perc (raw): {ram.perc.last(format=False)}")


if __name__ == "__main__":
    test()