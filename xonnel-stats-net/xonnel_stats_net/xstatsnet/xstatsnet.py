from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import time
import psutil

from xonnel_stats_data import XStatsData


class XStatsNet:
    def __init__(self):
        self.last_data = None
        self.last_time = None

        self.init()

    def init(self):
        self.sent: XStatsData = XStatsData(unit="GiB")
        self.recv: XStatsData = XStatsData(unit="GiB")
        self.up  : XStatsData = XStatsData(unit="MiB/s")
        self.down: XStatsData = XStatsData(unit="MiB/s")
        self.rate: XStatsData = XStatsData(unit="MiB/s")

    def _GiB(self, bytes: int) -> float:
        return float(bytes) / (1024 ** 3)

    def _MiB(self, bytes: int) -> float:
        return float(bytes) / (1024 ** 2)

    def getdata(self):
        return psutil.net_io_counters()

    def getsent(self) -> float:
        data = self.getdata()
        return self._GiB(data.bytes_sent)

    def getrecv(self) -> float:
        data = self.getdata()
        return self._GiB(data.bytes_recv)

    def getup(self) -> float:
        data = self.getdata()
        now = time.time()

        if self.last_data is None or self.last_time is None:
            return 0.0

        dt = now - self.last_time
        if dt <= 0:
            return 0.0

        dbytes = data.bytes_sent - self.last_data.bytes_sent
        return self._MiB(dbytes) / dt

    def getdown(self) -> float:
        data = self.getdata()
        now = time.time()

        if self.last_data is None or self.last_time is None:
            return 0.0

        dt = now - self.last_time
        if dt <= 0:
            return 0.0

        dbytes = data.bytes_recv - self.last_data.bytes_recv
        return self._MiB(dbytes) / dt

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        data = self.getdata()
        now = time.time()

        sent = self._GiB(data.bytes_sent)
        recv = self._GiB(data.bytes_recv)

        if self.last_data is None or self.last_time is None:
            up = 0.0
            down = 0.0
        else:
            dt = now - self.last_time
            if dt <= 0:
                up = 0.0
                down = 0.0
            else:
                up = self._MiB(data.bytes_sent - self.last_data.bytes_sent) / dt
                down = self._MiB(data.bytes_recv - self.last_data.bytes_recv) / dt

        self.sent.append(data=sent)
        self.recv.append(data=recv)
        self.up.append(data=up)
        self.down.append(data=down)
        self.rate.append(data=up + down)

        self.last_data = data
        self.last_time = now

    def update_data(self):
        self.sent.update()
        self.recv.update()
        self.up.update()
        self.down.update()
        self.rate.update()

def test():
    net = XStatsNet()

    import time
    for i in range(10):
        time.sleep(3)
        net.update()

        print(f"sent: {net.sent.last()}")
        print(f"recv: {net.recv.last()}")
        print(f"up:   {net.up.last()}")
        print(f"down: {net.down.last()}")
        print(f"rate: {net.rate.last()}")
        print(f"sent (raw): {net.sent.last(format=False)}")
        print(f"recv (raw): {net.recv.last(format=False)}")
        print(f"up   (raw): {net.up.last(format=False)}")
        print(f"down (raw): {net.down.last(format=False)}")
        print(f"rate (raw): {net.rate.last(format=False)}")
        print("-" * 40)


if __name__ == "__main__":
    test()