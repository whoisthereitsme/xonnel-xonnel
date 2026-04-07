from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xplatonic import XPlatonic


PHI = (1.0 + np.sqrt(5.0)) / 2.0
A = 1.0 / PHI
B = 1.0


class XDodec(XPlatonic):
    VERTS = np.array([
        (-B, -B, -B),
        (-B, -B,  B),
        (-B,  B, -B),
        (-B,  B,  B),
        ( B, -B, -B),
        ( B, -B,  B),
        ( B,  B, -B),
        ( B,  B,  B),

        ( 0, -A, -PHI),
        ( 0, -A,  PHI),
        ( 0,  A, -PHI),
        ( 0,  A,  PHI),

        (-A, -PHI, 0),
        (-A,  PHI, 0),
        ( A, -PHI, 0),
        ( A,  PHI, 0),

        (-PHI, 0, -A),
        ( PHI, 0, -A),
        (-PHI, 0,  A),
        ( PHI, 0,  A),
    ], dtype=np.float64)

    POLYS = [
        (0, 8, 10, 2, 16),
        (0, 16, 18, 1, 12),
        (0, 12, 14, 4, 8),
        (1, 9, 11, 3, 18),
        (1, 12, 14, 5, 9),
        (2, 10, 6, 17, 16),
        (3, 11, 7, 15, 13),
        (2, 13, 3, 18, 16),
        (4, 8, 10, 6, 17),
        (5, 9, 11, 7, 19),
        (4, 14, 5, 19, 17),
        (6, 17, 19, 7, 15),
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
        norms = np.linalg.norm(XDodec.VERTS, axis=1, keepdims=True)
        return (XDodec.VERTS / norms) * self.size

    def getfaces(self):
        verts = self.verts.tolist()
        faces = []

        for poly in XDodec.POLYS:
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
        lines = ["o XDodec"]
        for v in self.verts:
            lines.append(f"v {v[0]} {v[1]} {v[2]}")
        for f in self.faces:
            lines.append(f"f {f[0]+1} {f[1]+1} {f[2]+1}")
        return "\n".join(lines) + "\n"