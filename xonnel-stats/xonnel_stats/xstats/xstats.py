from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from xonnel_stats_cpu   import XStatsCpu
from xonnel_stats_gpu   import XStatsGpu
from xonnel_stats_ram   import XStatsRam
from xonnel_stats_vram  import XStatsVram
from xonnel_stats_disk  import XStatsDisks
from xonnel_stats_net   import XStatsNet
from xonnel_stats_win   import XStatsWin



    



class XStats:
    def __init__(self):
        self.init()

    def init(self):
        self.cpu:        XStatsCpu   = XStatsCpu()
        self.gpu:        XStatsGpu   = XStatsGpu()
        self.ram:        XStatsRam   = XStatsRam()
        self.vram:       XStatsVram  = XStatsVram()
        self.disks:      XStatsDisks = XStatsDisks()
        self.net:        XStatsNet   = XStatsNet()
        self.win:        XStatsWin   = XStatsWin()


    def update(self):
        self.cpu.update()
        self.gpu.update()
        self.ram.update()
        self.vram.update()
        self.disks.update()
        self.net.update()
        self.win.update()




def test():
    stats = XStats()

    import time
    for i in range(60):
        time.sleep(1)
        stats.update()

        print(f"cpu:        {stats.cpu.core.perc.last()}")
        print(f"gpu:        {stats.gpu.perc.last()}")
        print(f"ram:        {stats.ram.perc.last()}")
        print(f"vram:       {stats.vram.perc.last()}")
        print(f"C://:       {stats.disks.disks['C'].perc.last()}")
        print(f"net up:     {stats.net.up.last()}")
        print(f"net down:   {stats.net.down.last()}")
        print(f"net rate:   {stats.net.rate.last()}")
        print(f"win:        {stats.win.rate.last()}")

        print("-" * 40)


if __name__ == "__main__":
    test()