from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetClockInfo, nvmlDeviceGetTemperature, NVML_CLOCK_GRAPHICS, NVML_TEMPERATURE_GPU

from xonnel_stats_data import XStatsData


class XStatsGpu:
    def __init__(self):
        self.nvml()
        self.init()

    def nvml(self):
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(0)

    def init(self):
        self.perc: XStatsData = XStatsData(unit="%")
        self.freq: XStatsData = XStatsData(unit="GHz")
        self.temp: XStatsData = XStatsData(unit="°C")

    def _GHz(self, MHz: float) -> float:
        return float(MHz) / 1000.0

    def getperc(self) -> float:
        data = nvmlDeviceGetUtilizationRates(self.handle)
        return float(data.gpu)

    def getfreq(self) -> float:
        MHz = nvmlDeviceGetClockInfo(self.handle, NVML_CLOCK_GRAPHICS)
        return self._GHz(MHz)

    def gettemp(self) -> float:
        return float(nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU))

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        self.perc.append(data=self.getperc())
        self.freq.append(data=self.getfreq())
        self.temp.append(data=self.gettemp())

    def update_data(self):
        self.perc.update()
        self.freq.update()
        self.temp.update()

    def close(self):
        try:
            nvmlShutdown()
        except Exception:
            ...

    def __del__(self):
        self.close()


def test():
    gpu = XStatsGpu()
    gpu.update()

    print(f"perc: {gpu.perc.last()}")
    print(f"freq: {gpu.freq.last()}")
    print(f"temp: {gpu.temp.last()}")

    print(f"perc (raw): {gpu.perc.last(format=False)}")
    print(f"freq (raw): {gpu.freq.last(format=False)}")
    print(f"temp (raw): {gpu.temp.last(format=False)}")


if __name__ == "__main__":
    test()