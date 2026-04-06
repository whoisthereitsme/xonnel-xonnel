from .pnoize2 import PNoize2
import numpy as np








class RNoize2:
    def __init__(
        self,
        size: tuple = (512, 512),
        offset: tuple = (0.0, 0.0),
        seed: int = 0,
        scale: float = 64.0,
        octs: int = 1,
        pers: float = 0.5,
        lacu: float = 2.0,
        norm: tuple = (0.0, 1.0),
    ):
        self.size = size
        self.offset = offset
        self.seed = seed
        self.scale = scale
        self.octs = octs
        self.pers = pers
        self.lacu = lacu
        self.norm = norm

        self.noize = self._generate()

    def _generate(self):
        arr = PNoize2(
            size=self.size,
            offset=self.offset,
            seed=self.seed,
            scale=self.scale,
            octs=self.octs,
            pers=self.pers,
            lacu=self.lacu,
            norm=(0.0, 1.0),
        ).noize

        arr = 1.0 - np.abs(arr * 2.0 - 1.0)
        arr = arr * arr

        norm0, norm1 = self.norm
        arr = norm0 + arr * (norm1 - norm0)

        return arr.astype(np.float32, copy=False)
    
