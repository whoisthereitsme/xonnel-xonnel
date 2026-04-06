from pathlib import Path

import numpy as np
from PIL import Image

from xonnel_noize import XNoize
from xonnel_voxel import XVoxel
from xonnel_file import XFile


ROOT = Path(r"C:\Code\Python\Packages\xonnel-noize\xonnel_noize\xnoize\tests")


def save_png(data, path):
    arr = np.asarray(data, dtype=np.float32)
    arr = arr.astype(np.uint8)
    img = Image.fromarray(arr, mode="L")
    XFile.save(path=path, data=img)


def save_obj(data, path, threshold=0.5, voxel_size=1.0):
    voxel = XVoxel(array=data, tres=threshold, size=(voxel_size, voxel_size, voxel_size), origin=(0.0, 0.0, 0.0))
    XFile.save(path=path, data=voxel.obj)


def main():
    seed = 123
    scale = 64.0
    octs = 6
    pers = 0.5
    lacu = 2.0
    nor2 = (0.0, 255.0)
    nor3 = (0.0, 1.0)
    of2d = (0.0, 0.0)
    of3d = (0.0, 0.0, 0.0)

    size2 = (8192, 8192)
    size3 = (256, 256, 256)

    print("gen perl2"); save_png(XNoize.perl2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "perl2.png")
    print("gen simp2"); save_png(XNoize.simp2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "simp2.png")
    print("gen worl2"); save_png(XNoize.worl2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "worl2.png")

    print("gen perl3"); save_obj(XNoize.perl3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "perl3.obj")
    print("gen simp3"); save_obj(XNoize.simp3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "simp3.obj")
    print("gen worl3"); save_obj(XNoize.worl3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "worl3.obj")

    print("gen ridg2"); save_png(XNoize.ridg2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "ridg2.png")
    print("gen ridg3"); save_obj(XNoize.ridg3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "ridg3.obj")

    print("gen bill2"); save_png(XNoize.bill2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "bill2.png")
    print("gen bill3"); save_obj(XNoize.bill3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "bill3.obj")

    print("gen terr2"); save_png(XNoize.terr2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "terr2.png")
    print("gen terr3"); save_obj(XNoize.terr3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "terr3.obj")

    print("gen crak2"); save_png(XNoize.crak2(size=size2, offset=of2d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor2), ROOT / "crak2.png")
    print("gen crak3"); save_obj(XNoize.crak3(size=size3, offset=of3d, seed=seed, scale=scale, octs=octs, pers=pers, lacu=lacu, norm=nor3), ROOT / "crak3.obj")

    print("done")


if __name__ == "__main__":
    main()