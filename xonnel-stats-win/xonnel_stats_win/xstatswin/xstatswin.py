from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import ctypes

from xonnel_stats_data import XStatsData


class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),

        ("dmPositionX", ctypes.c_long),
        ("dmPositionY", ctypes.c_long),
        ("dmDisplayOrientation", ctypes.c_ulong),
        ("dmDisplayFixedOutput", ctypes.c_ulong),

        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong),
    ]


class XStatsWin:
    ENUM_CURRENT_SETTINGS = -1

    def __init__(self):
        self.init()

    def init(self):
        self.width : XStatsData = XStatsData(unit="px")
        self.height: XStatsData = XStatsData(unit="px")
        self.area  : XStatsData = XStatsData(unit="px^2")
        self.rate  : XStatsData = XStatsData(unit="Hz")
        self.depth : XStatsData = XStatsData(unit="bpp")

    def getdata(self) -> DEVMODE | None:
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(DEVMODE)

        ok = ctypes.windll.user32.EnumDisplaySettingsW(None, self.ENUM_CURRENT_SETTINGS, ctypes.byref(devmode))
        if not ok:
            return None
        return devmode

    def getwidth(self) -> float:
        data = self.getdata()
        if data is None:
            return 0.0
        return float(data.dmPelsWidth)

    def getheight(self) -> float:
        data = self.getdata()
        if data is None:
            return 0.0
        return float(data.dmPelsHeight)

    def getarea(self) -> float:
        data = self.getdata()
        if data is None:
            return 0.0
        return float(data.dmPelsWidth * data.dmPelsHeight)

    def getrate(self) -> float:
        data = self.getdata()
        if data is None:
            return 0.0
        return float(data.dmDisplayFrequency)

    def getdepth(self) -> float:
        data = self.getdata()
        if data is None:
            return 0.0
        return float(data.dmBitsPerPel)

    def update(self):
        self.append_data()
        self.update_data()

    def append_data(self):
        self.width.append(data=self.getwidth())
        self.height.append(data=self.getheight())
        self.area.append(data=self.getarea())
        self.rate.append(data=self.getrate())
        self.depth.append(data=self.getdepth())

    def update_data(self):
        self.width.update()
        self.height.update()
        self.area.update()
        self.rate.update()
        self.depth.update()


def test():
    win = XStatsWin()
    win.update()

    print(f"width: {win.width.last()}")
    print(f"height: {win.height.last()}")
    print(f"area: {win.area.last()}")
    print(f"rate: {win.rate.last()}")
    print(f"depth: {win.depth.last()}")

    print(f"width (raw): {win.width.last(format=False)}")
    print(f"height (raw): {win.height.last(format=False)}")
    print(f"area (raw): {win.area.last(format=False)}")
    print(f"rate (raw): {win.rate.last(format=False)}")
    print(f"depth (raw): {win.depth.last(format=False)}")


if __name__ == "__main__":
    test()