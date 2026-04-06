from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...


# base noize 
from .pnoize2 import PNoize2
from .pnoize3 import PNoize3
from .snoize2 import SNoize2
from .snoize3 import SNoize3
from .wnoize2 import WNoize2
from .wnoize3 import WNoize3

# derrived noize from base noize
from .rnoize2 import RNoize2
from .rnoize3 import RNoize3
from .bnoize2 import BNoize2
from .bnoize3 import BNoize3
from .tnoize2 import TNoize2
from .tnoize3 import TNoize3
from .cnoize2 import CNoize2
from .cnoize3 import CNoize3


class XNoize:
    perlin2 = PNoize2
    perlin3 = PNoize3
    simplex2 = SNoize2
    simplex3 = SNoize3
    worley2 = WNoize2
    worley3 = WNoize3
    ridged2 = RNoize2
    ridged3 = RNoize3

    @staticmethod
    def perl2(size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return PNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def perl3(size=(64,64,64), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return PNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def simp2(size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return SNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def simp3(size=(64,64,64), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return SNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def worl2(size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return WNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def worl3(size=(64,64,64), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return WNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def ridg2(size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return RNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @staticmethod
    def ridg3(size=(64,64,64), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return RNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def bill2(cls, size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return BNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def bill3(cls, size=(128,128,128), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return BNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def terr2(cls, size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return TNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def terr3(cls, size=(128,128,128), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return TNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def crak2(cls, size=(512,512), offset=(0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return CNoize2(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize

    @classmethod
    def crak3(cls, size=(128,128,128), offset=(0.0,0.0,0.0), seed=0, scale=64.0, octs=1, pers=0.5, lacu=2.0, norm=(0.0,1.0)):
        return CNoize3(size=size, offset=offset, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=norm).noize