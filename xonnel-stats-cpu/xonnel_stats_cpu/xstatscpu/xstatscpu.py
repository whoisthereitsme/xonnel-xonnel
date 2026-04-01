from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import psutil

from xonnel_stats_data import XStatsData
from xonnel_stat import XStat

class XStatsCpuCore:
    def __init__(self, cpu:XStatsCpu=None, id:int|None=None):
        self.cpu: XStatsCpu = cpu
        self.id: int|None = id

        self.init()

    def init(self):
        self.perc = XStatsData(unit="%")
        self.freq = XStatsData(unit="GHz")
        self.time = XStatsData(unit="s")

    def _GHz(self, MHz: float) -> float:
        return float(MHz) / 1000.0

    def _percpu(self) -> bool:
        return self.id is not None
    
    def getperc(self) -> float:
        # use the one stored it updates there ONCE per update
        # then each core can just get its value from there instead of calling psutil again which would return 0.0 
        # since it needs to be called with interval=None and percpu=True to get the correct value for each core, 
        # but then it returns a list of values for each core, so we need to handle that case in the core class 
        # return the correct value for each core based on its id
        if self._percpu():
            return float(self.cpu.perc[self.id])
        return XStat.mean(self.cpu.perc)

    def getfreq(self) -> float:
        percpu = self._percpu()

        if percpu:
            data = psutil.cpu_freq(percpu=True)

            if isinstance(data, list) and self.id < len(data):
                return self._GHz(data[self.id].current)

            total = psutil.cpu_freq(percpu=False)
            if total is None:
                return 0.0
            return self._GHz(total.current)

        data = psutil.cpu_freq(percpu=False)
        if data is None:
            return 0.0
        return self._GHz(data.current)

    def gettime(self) -> float:
        percpu = self._percpu()

        if percpu:
            data = psutil.cpu_times(percpu=True)
            if self.id >= len(data):
                return 0.0
            return float(data[self.id].user)

        data = psutil.cpu_times(percpu=False)
        return float(data.user)

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        self.perc.append(data=self.getperc())
        self.freq.append(data=self.getfreq())
        self.time.append(data=self.gettime())

    def update_data(self):
        self.perc.update()
        self.freq.update()
        self.time.update()


class XStatsCpu:
    def __init__(self):
        self.init()

    def init(self):
        self.core: XStatsCpuCore = XStatsCpuCore(cpu=self, id=None)
        self.cores: dict[int, XStatsCpuCore] = {}

        for id in self.getids():
            core = XStatsCpuCore(cpu=self, id=id)
            self.cores[id] = core
            setattr(self, f"cpu{id}", core)

    @classmethod
    def getids(cls) -> list[int]:
        n = psutil.cpu_count(logical=True)
        return list(range(n)) if n else []
    
    def getperc(self) -> list[float]:     
        # this one can't be called in any of the cores becouse repeated call return 0.0 
        # since it needs to be called with interval=None and percpu=True to get the correct value for each core
        # but then it returns a list of values for each core, so we need to handle that case in the core class 
        # and return the correct value for each core based on its id
        return psutil.cpu_percent(interval=None, percpu=True)

    def update(self):
        self.perc = self.getperc()
        self.core.update()
        for core in self.cores.values():
            core.update()








