from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xplatonic import XPlatonic


class XCubic(XPlatonic):
    VERTS = np.array([
        (-1, -1, -1),
        ( 1, -1, -1),
        ( 1,  1, -1),
        (-1,  1, -1),
        (-1, -1,  1),
        ( 1, -1,  1),
        ( 1,  1,  1),
        (-1,  1,  1),
    ], dtype=np.float64)

    POLYS = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
        (0, 3, 7, 4),
        (1, 5, 6, 2),
    ]

    def __init__(self, size: float = 1.0):
        super().__init__(size=size)
        self.init()

    def init(self):
        self.verts = self.getverts()
        self.faces = self.getfaces()
        self.edges = self.getedges()
        self.object = self.getobject()

    def getverts(self):
        return XCubic.VERTS.copy() * self.size

    def getfaces(self):
        verts = self.verts.tolist()
        faces = []

        for poly in XCubic.POLYS:
            poly = list(poly)
            pverts = np.array([verts[i] for i in poly], dtype=np.float64)
            center = pverts.mean(axis=0)

            cidx = len(verts)
            verts.append(center.tolist())

            n = len(poly)
            for i in range(n):
                a = poly[i]
                b = poly[(i + 1) % n]
                faces.append((cidx, a, b))

        self.verts = np.array(verts, dtype=np.float64)
        return np.array(faces, dtype=np.int32)

    def getedges(self):
        edges = set()
        for f in self.faces:
            for i in range(3):
                a = int(f[i])
                b = int(f[(i + 1) % 3])
                edges.add(tuple(sorted((a, b))))
        return np.array(sorted(edges), dtype=np.int32)

    def getobject(self):
        lines = ["o XCubic"]
        for v in self.verts:
            lines.append(f"v {v[0]} {v[1]} {v[2]}")
        for f in self.faces:
            lines.append(f"f {f[0]+1} {f[1]+1} {f[2]+1}")
        return "\n".join(lines) + "\n"
    


