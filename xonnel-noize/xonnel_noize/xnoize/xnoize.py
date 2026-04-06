from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...



from pathlib import Path
import ctypes
import numpy as np


class XNoize:
    DLL = None
    def __init__(self, size:tuple=(4096, 4096), offset:tuple=(0, 0), seed:int=0, scale:float=1.0, octs:int=6, lacu:float=2.0, pers:float=0.5, norm:tuple=(0.0, 1.0)):
        self.size = size
        self.offset = offset
        self.seed = seed
        self.scale = scale 
        self.octs = octs
        self.lacu = lacu
        self.pers = pers
        self.norm = norm

        self.noize = self._noize()

    @classmethod
    def _dll(cls):
        if cls.DLL is None:
            path = Path(__file__).with_name("xnoize.dll")
            cls.DLL = ctypes.CDLL(str(path))

            cls.DLL.xnoize_perlin.argtypes = [
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
            cls.DLL.xnoize_perlin.restype = None

        return cls.DLL

    def _noize(self):
        w = int(self.size[0])
        h = int(self.size[1])
        offx = float(self.offset[0])
        offy = float(self.offset[1])
        norm0 = float(self.norm[0])
        norm1 = float(self.norm[1])

        if w <= 0:
            raise ValueError(f"invalid width: {w}")
        if h <= 0:
            raise ValueError(f"invalid height: {h}")
        if self.scale <= 0:
            raise ValueError(f"invalid scale: {self.scale}")
        if self.octs <= 0:
            raise ValueError(f"invalid octs: {self.octs}")
        if self.lacu <= 0:
            raise ValueError(f"invalid lacu: {self.lacu}")

        dll = self._dll()

        noize = np.empty((h, w), dtype=np.float32)

        dll.xnoize_perlin(
            noize.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            w,
            h,
            ctypes.c_uint32(self.seed),
            ctypes.c_float(self.scale),
            self.octs,
            ctypes.c_float(self.pers),
            ctypes.c_float(self.lacu),
            ctypes.c_float(offx),
            ctypes.c_float(offy),
            ctypes.c_float(norm0),
            ctypes.c_float(norm1),
        )

        return noize




















import time
from noise import pnoise2


def pytnoise(
        size=(8192, 8192),
        offset=(0, 0),
        seed=123,
        scale=64.0,
        octs=6,
        lacu=2.0,
        pers=0.5,
        norm=(0.0, 1.0),
    ):
    w = int(size[0])
    h = int(size[1])
    offx = float(offset[0])
    offy = float(offset[1])
    norm0 = float(norm[0])
    norm1 = float(norm[1])

    if w <= 0:
        raise ValueError(f"invalid width: {w}")
    if h <= 0:
        raise ValueError(f"invalid height: {h}")
    if scale <= 0:
        raise ValueError(f"invalid scale: {scale}")
    if octs <= 0:
        raise ValueError(f"invalid octs: {octs}")
    if lacu <= 0:
        raise ValueError(f"invalid lacu: {lacu}")

    noize = np.empty((h, w), dtype=np.float32)

    mn = None
    mx = None

    for y in range(h):
        for x in range(w):
            sx = (x + offx) / scale
            sy = (y + offy) / scale

            val = pnoise2(
                sx,
                sy,
                octaves=octs,
                persistence=pers,
                lacunarity=lacu,
                repeatx=1024,
                repeaty=1024,
                base=seed,
            )

            noize[y, x] = val

            if mn is None or val < mn:
                mn = val
            if mx is None or val > mx:
                mx = val

    rng = mx - mn
    if rng > 0.0:
        noize = norm0 + ((noize - mn) / rng) * (norm1 - norm0)
    else:
        noize.fill((norm0 + norm1) * 0.5)

    return noize.astype(np.float32, copy=False)










import time
import numpy as np
from PIL import Image


def to_png(data, path):

    arr = np.asarray(data)
    arr = np.clip(arr, 0.0, 255.0)
    arr = arr.astype(np.uint8)
    img = Image.fromarray(arr, mode="L")
    img.save(path)


def test(size=(None, None)):
    t0 = time.perf_counter()
    dllnoize = XNoize(
        size=size,
        offset=(0, 0),
        seed=123,
        scale=64.0,
        octs=6,
        lacu=2.0,
        pers=0.5,
        norm=(0.0, 255.0),
    ).noize
    t1 = time.perf_counter()
    cpptime = t1 - t0

    t0 = time.perf_counter()
    pytnoize = pytnoise(
        size=size,
        offset=(0, 0),
        seed=123,
        scale=64.0,
        octs=6,
        lacu=2.0,
        pers=0.5,
        norm=(0.0, 255.0),
    )
    t1 = time.perf_counter()
    pyttime = t1 - t0
    print(f"py:{pyttime:.2f}s cpp:{cpptime:.2f}s size={size} ratio={pyttime / cpptime:.2f}")
    # save ONLY cpp version (as you asked)
    to_png(dllnoize, f"C:\\Code\\Python\\Packages\\xonnel-noize\\xonnel_noize\\xnoize\\tests\\cpp_{size[0]}x{size[1]}.png")

    


if __name__ == "__main__":
    test(size=(16000, 16000))