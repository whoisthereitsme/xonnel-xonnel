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


def save_obj_voxels(data, path, threshold=0.5, voxel_size=1.0):
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

                # -X
                if not is_solid(x - 1, y, z):
                    add_face(
                        (x0, y0, z0),
                        (x0, y0, z1),
                        (x0, y1, z1),
                        (x0, y1, z0),
                    )

                # +X
                if not is_solid(x + 1, y, z):
                    add_face(
                        (x1, y0, z0),
                        (x1, y1, z0),
                        (x1, y1, z1),
                        (x1, y0, z1),
                    )

                # -Y
                if not is_solid(x, y - 1, z):
                    add_face(
                        (x0, y0, z0),
                        (x1, y0, z0),
                        (x1, y0, z1),
                        (x0, y0, z1),
                    )

                # +Y
                if not is_solid(x, y + 1, z):
                    add_face(
                        (x0, y1, z0),
                        (x0, y1, z1),
                        (x1, y1, z1),
                        (x1, y1, z0),
                    )

                # -Z
                if not is_solid(x, y, z - 1):
                    add_face(
                        (x0, y0, z0),
                        (x0, y1, z0),
                        (x1, y1, z0),
                        (x1, y0, z0),
                    )

                # +Z
                if not is_solid(x, y, z + 1):
                    add_face(
                        (x0, y0, z1),
                        (x1, y0, z1),
                        (x1, y1, z1),
                        (x0, y1, z1),
                    )

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

    print("gen perl2")
    perl2 = XNoize.perl2(
        size=size2,
        offset=(0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_png(perl2, ROOT / "perl2.png")

    print("gen simp2")
    simp2 = XNoize.simp2(
        size=size2,
        offset=(0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_png(simp2, ROOT / "simp2.png")

    print("gen worl2")
    worl2 = XNoize.worl2(
        size=size2,
        offset=(0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_png(worl2, ROOT / "worl2.png")

    print("gen perl3")
    perl3 = XNoize.perl3(
        size=size3,
        offset=(0.0, 0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_obj_voxels(perl3, ROOT / "perl3.obj", threshold=0.5, voxel_size=1.0)

    print("gen simp3")
    simp3 = XNoize.simp3(
        size=size3,
        offset=(0.0, 0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_obj_voxels(simp3, ROOT / "simp3.obj", threshold=0.5, voxel_size=1.0)

    print("gen worl3")
    worl3 = XNoize.worl3(
        size=size3,
        offset=(0.0, 0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_obj_voxels(worl3, ROOT / "worl3.obj", threshold=0.5, voxel_size=1.0)

    print("done")

    print("gen ridg2")
    ridg2 = XNoize.ridg2(
        size=size2,
        offset=(0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_png(ridg2, ROOT / "ridg2.png")

    print("gen ridg3")
    ridg3 = XNoize.ridg3(
        size=size3,
        offset=(0.0, 0.0, 0.0),
        seed=seed,
        scale=scale,
        octs=octs,
        pers=pers,
        lacu=lacu,
        norm=norm,
    )
    save_obj_voxels(ridg3, ROOT / "ridg3.obj", threshold=0.5, voxel_size=1.0)


if __name__ == "__main__":
    main()