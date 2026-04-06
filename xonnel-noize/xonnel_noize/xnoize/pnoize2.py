from pathlib import Path
import ctypes
import numpy as np


class PNoize2:
    DLL = None

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

    @classmethod
    def _dll(cls):
        if cls.DLL is None:
            path = Path(__file__).resolve().with_name("pnoize2.dll")
            dll = ctypes.CDLL(str(path))

            dll.pnoize2.argtypes = [
                ctypes.POINTER(ctypes.c_float),   # out
                ctypes.c_size_t,                  # w
                ctypes.c_size_t,                  # h
                ctypes.c_uint32,                  # seed
                ctypes.c_float,                   # scale
                ctypes.c_size_t,                  # octs
                ctypes.c_float,                   # pers
                ctypes.c_float,                   # lacu
                ctypes.c_float,                   # offx
                ctypes.c_float,                   # offy
                ctypes.c_float,                   # norm0
                ctypes.c_float,                   # norm1
            ]
            dll.pnoize2.restype = None

            cls.DLL = dll

        return cls.DLL

    def _generate(self):
        w, h = self.size
        offx, offy = self.offset
        norm0, norm1 = self.norm

        arr = np.empty((h, w), dtype=np.float32)

        self._dll().pnoize2(
            arr.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            w,
            h,
            self.seed,
            self.scale,
            self.octs,
            self.pers,
            self.lacu,
            offx,
            offy,
            norm0,
            norm1,
        )
        return arr