from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo







from xonnel_stats_data import XStatsData






class XStatsVram:
    def __init__(self, id:int=0):
        self.id = id

        self.nvml()
        self.init()

    def nvml(self):
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(self.id)

    def init(self):
        self.size: XStatsData = XStatsData(unit="GiB")
        self.used: XStatsData = XStatsData(unit="GiB")
        self.free: XStatsData = XStatsData(unit="GiB")
        self.perc: XStatsData = XStatsData(unit="%")

    def _GiB(self, bytes: int) -> float:
        return float(bytes) / (1024 ** 3)

    def _per(self, val: float, max: float) -> float:
        if max == 0:
            return 0.0
        return (val / max) * 100.0

    def getdata(self):
        return nvmlDeviceGetMemoryInfo(self.handle)

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
        used = self._GiB(data.used)
        total = self._GiB(data.total)
        return self._per(used, total)

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

    def _close(self):
        try:
            nvmlShutdown()
        except Exception:
            ...

    def __del__(self):
        self._close()


def test():
    vram = XStatsVram(id=0)
    vram.update()

    print(f"size: {vram.size.last()}")
    print(f"used: {vram.used.last()}")
    print(f"free: {vram.free.last()}")
    print(f"perc: {vram.perc.last()}")

    print(f"size (raw): {vram.size.last(format=False)}")
    print(f"used (raw): {vram.used.last(format=False)}")
    print(f"free (raw): {vram.free.last(format=False)}")
    print(f"perc (raw): {vram.perc.last(format=False)}")


if __name__ == "__main__":
    test()