from pathlib import Path
import ctypes
import numpy as np


class WNoize2:
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
            path = Path(__file__).resolve().with_name("wnoize2.dll")
            dll = ctypes.CDLL(str(path))

            dll.wnoize2.argtypes = [
                ctypes.POINTER(ctypes.c_float),
                ctypes.c_size_t,
                ctypes.c_size_t,
                ctypes.c_uint32,
                ctypes.c_float,
                ctypes.c_size_t,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
            ]
            dll.wnoize2.restype = None

            cls.DLL = dll

        return cls.DLL

    def _generate(self):
        w, h = self.size
        offx, offy = self.offset
        norm0, norm1 = self.norm

        arr = np.empty((h, w), dtype=np.float32)

        self._dll().wnoize2(
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