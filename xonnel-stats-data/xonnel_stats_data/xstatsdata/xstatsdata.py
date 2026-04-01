from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...







import time
from xonnel_stat import XStat











class XStatsPair:
    TIME:float = 3600.0 * 8      # seconds to keep data in history before it gets removed, default is 8 hours

    def __init__(self, data=None):
        self.time = self._now()
        self.data = data

    def _now(self):
        return time.time()
    
    def aged(self):
        return self.age() >= XStatsPair.TIME

    def age(self):
        return self._now() - self.time








class XStatsData:
    def __init__(self, unit:str=None):
        self.unit = unit

        self.init()
  

    def init(self):
        self.history = [] 

    def add(self, data=None):
        self.history.append(XStatsPair(data=data))

    def update(self):
        self.history = [pair for pair in self.history if not pair.aged()]

    def filter(self, time:float=1.0):
        return [pair.data for pair in self.history if pair.age() <= time]

    def mean(self, time:float=10.0):
        data = self.filter(time=time)
        if data is not None:
            return XStat.mean(data=data)
        return None
        
    def min(self, time:float=60.0):
        data = self.filter(time=time)
        if data is not None:
            return XStat.min(data=data)
        return None
    
    def max(self, time:float=60.0):
        data = self.filter(time=time)
        if data is not None:
            return XStat.max(data=data)
        return None
            