from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...



from .pnoize2 import PNoize2
from .pnoize3 import PNoize3
from .snoize2 import SNoize2
from .snoize3 import SNoize3
from .wnoize2 import WNoize2
from .wnoize3 import WNoize3
from .rnoize2 import RNoize2
from .rnoize3 import RNoize3




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
    def perl2(
        size: tuple = (512, 512),
        offset: tuple = (0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return PNoize2(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize

    @staticmethod
    def perl3(
        size: tuple = (64, 64, 64),
        offset: tuple = (0.0, 0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return PNoize3(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize

    @staticmethod
    def simp2(
        size: tuple = (512, 512),
        offset: tuple = (0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return SNoize2(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize

    @staticmethod
    def simp3(
        size: tuple = (64, 64, 64),
        offset: tuple = (0.0, 0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return SNoize3(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize

    @staticmethod
    def worl2(
        size: tuple = (512, 512),
        offset: tuple = (0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return WNoize2(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize

    @staticmethod
    def worl3(
        size: tuple = (64, 64, 64),
        offset: tuple = (0.0, 0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return WNoize3(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize
    
    @staticmethod
    def ridg2(
        size: tuple = (512, 512),
        offset: tuple = (0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return RNoize2(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize
    
    @staticmethod
    def ridg3(
        size: tuple = (64, 64, 64),
        offset: tuple = (0.0, 0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        return RNoize3(
            size=size,
            offset=offset,
            seed=seed,
            scale=scale,
            octs=octs,
            pers=pers,
            lacu=lacu,
            norm=norm,
        ).noize