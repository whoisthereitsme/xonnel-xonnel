from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from xonnel_stats_cpu   import XStatsCpu
from xonnel_stats_gpu   import XStatsGpu
from xonnel_stats_ram   import XStatsRam
from xonnel_stats_vram  import XStatsVram
from xonnel_stats_disk  import XStatsDisk
from xonnel_stats_net   import XStatsNet
from xonnel_stats_win   import XStatsWin







class XStats:
    def __init__(self):
        self.init()

    def init(self):
        self.cpu  = XStatsCpu()
        self.gpu  = XStatsGpu()
        self.ram  = XStatsRam()
        self.vram = XStatsVram()
        self.disk = XStatsDisk()
        self.net  = XStatsNet()
        self.win  = XStatsWin()


    def update(self):
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.vram.update()
        self.disk.update()
        self.net.update()
        self.win.update()

