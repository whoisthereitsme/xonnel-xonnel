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
    def __init__(self, unit:str=""):
        self.unit: str = unit

        self.init()
  

    def init(self):
        self.history: list[XStatsPair] = [] 

    def append(self, data=None):
        self.history.append(XStatsPair(data=data))

    def update(self):                 # not using comprehension here since then i cannot break early!!
        for pair in self.history:
            if pair.aged():
                self.history.remove(pair)
            else:
                break

    def filter(self, time:float=1.0): # not using comprehension here since then i cannot break early!!
        selected = []
        for pair in self.history:
            if pair.age() > time:
                selected.append(pair.data)
            else:
                break
        return selected

    def mean(self, time:float=10.0, format=True):
        data = self.filter(time=time)
        value = XStat.median(data=data)
        return self._format(value=value, format=format)
    
    def avg(self, time:float=10.0, format=True):
        data = self.filter(time=time)
        value = XStat.mean(data=data)
        return self._format(value=value, format=format)
        
    def min(self, time:float=60.0, format=True):
        data = self.filter(time=time)
        value = XStat.min(data=data)
        return self._format(value=value, format=format)

    def max(self, time:float=60.0, format=True):
        data = self.filter(time=time)
        value = XStat.max(data=data)
        return self._format(value=value, format=format)
    
    def last(self, format=True):
        if len(self.history) > 0:
            value = self.history[-1].data
            return self._format(value=value, format=format)
        return self._format(value=None, format=format)
    
    def _format(self, value:float=None, format=True):
        if value is None:
            return "N/A"
        value = round(value, 2)
        if format==True:
            return f"{value} {self.unit}"
        return value

            