from pathlib import Path

import numpy as np
from PIL import Image

from xnoize import XNoize


ROOT = Path(r"C:\Code\Python\Packages\xonnel-noize\xonnel_noize\xnoize\tests")


def save_png(data, path):
    arr = np.asarray(data, dtype=np.float32)
    arr = np.clip(arr, 0.0, 1.0)
    arr = (arr * 255.0).astype(np.uint8)
    img = Image.fromarray(arr, mode="L")
    img.save(path)


def save_obj(data, path, threshold=0.5, voxel_size=1.0):
    arr = np.asarray(data, dtype=np.float32)
    solid = arr >= threshold

    d, h, w = solid.shape

    verts = []
    faces = []
    vert_map = {}

    def add_vertex(v):
        if v not in vert_map:
            vert_map[v] = len(verts) + 1
            verts.append(v)
        return vert_map[v]

    def add_face(v0, v1, v2, v3):
        i0 = add_vertex(v0)
        i1 = add_vertex(v1)
        i2 = add_vertex(v2)
        i3 = add_vertex(v3)
        faces.append((i0, i1, i2, i3))

    s = float(voxel_size)

    def is_solid(x, y, z):
        if x < 0 or x >= w or y < 0 or y >= h or z < 0 or z >= d:
            return False
        return bool(solid[z, y, x])

    for z in range(d):
        for y in range(h):
            for x in range(w):
                if not solid[z, y, x]:
                    continue

                x0 = x * s
                x1 = (x + 1) * s
                y0 = y * s
                y1 = (y + 1) * s
                z0 = z * s
                z1 = (z + 1) * s

                if not is_solid(x - 1, y, z):
                    add_face((x0, y0, z0),(x0, y0, z1),(x0, y1, z1),(x0, y1, z0))
                if not is_solid(x + 1, y, z):
                    add_face((x1, y0, z0),(x1, y1, z0),(x1, y1, z1),(x1, y0, z1))
                if not is_solid(x, y - 1, z):
                    add_face((x0, y0, z0),(x1, y0, z0),(x1, y0, z1),(x0, y0, z1))
                if not is_solid(x, y + 1, z):
                    add_face((x0, y1, z0),(x0, y1, z1),(x1, y1, z1),(x1, y1, z0))
                if not is_solid(x, y, z - 1):
                    add_face((x0, y0, z0),(x0, y1, z0),(x1, y1, z0),(x1, y0, z0))
                if not is_solid(x, y, z + 1):
                    add_face((x0, y0, z1),(x1, y0, z1),(x1, y1, z1),(x0, y1, z1))

    with open(path, "w", encoding="utf-8") as f:
        f.write("# xnoize voxel mesh\n")
        f.write(f"# size: {w} {h} {d}\n")
        f.write(f"# threshold: {threshold}\n")
        f.write(f"# voxel_size: {voxel_size}\n")

        for x, y, z in verts:
            f.write(f"v {x} {y} {z}\n")

        for i0, i1, i2, i3 in faces:
            f.write(f"f {i0} {i1} {i2} {i3}\n")


def main():
    seed = 123
    scale = 64.0
    octs = 6
    pers = 0.5
    lacu = 2.0
    norm = (0.0, 1.0)

    size2 = (1024, 1024)
    size3 = (128, 128, 128)

    # ===== BASE =====
    print("gen perl2"); save_png(XNoize.perl2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"perl2.png")
    print("gen simp2"); save_png(XNoize.simp2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"simp2.png")
    print("gen worl2"); save_png(XNoize.worl2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"worl2.png")

    print("gen perl3"); save_obj(XNoize.perl3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"perl3.obj")
    print("gen simp3"); save_obj(XNoize.simp3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"simp3.obj")
    print("gen worl3"); save_obj(XNoize.worl3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"worl3.obj")

    # ===== RIDGED =====
    print("gen ridg2"); save_png(XNoize.ridg2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"ridg2.png")
    print("gen ridg3"); save_obj(XNoize.ridg3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"ridg3.obj")

    # ===== BILLOW =====
    print("gen bill2"); save_png(XNoize.bill2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"bill2.png")
    print("gen bill3"); save_obj(XNoize.bill3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"bill3.obj")

    # ===== TERRACE =====
    print("gen terr2"); save_png(XNoize.terr2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"terr2.png")
    print("gen terr3"); save_obj(XNoize.terr3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"terr3.obj")

    # ===== CRACK =====
    print("gen crak2"); save_png(XNoize.crak2(size=size2,offset=(0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"crak2.png")
    print("gen crak3"); save_obj(XNoize.crak3(size=size3,offset=(0.0,0.0,0.0),seed=seed,scale=scale,octs=octs,pers=pers,lacu=lacu,norm=norm), ROOT/"crak3.obj")

    print("done")


if __name__ == "__main__":
    main()