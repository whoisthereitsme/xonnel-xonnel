from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xplatonic import XPlatonic


class XOctah(XPlatonic):
    VERTS = np.array([
        ( 1, 0, 0),
        (-1, 0, 0),
        ( 0, 1, 0),
        ( 0,-1, 0),
        ( 0, 0, 1),
        ( 0, 0,-1),
    ], dtype=np.float64)

    FACES = np.array([
        (0, 2, 4),
        (2, 1, 4),
        (1, 3, 4),
        (3, 0, 4),
        (2, 0, 5),
        (1, 2, 5),
        (3, 1, 5),
        (0, 3, 5),
    ], dtype=np.int32)

    def __init__(self, size: float = 1.0):
        super().__init__(size=size)
        self.init()

    def init(self):
        self.verts = self.getverts()
        self.faces = self.getfaces()
        self.edges = self.getedges()
        self.object = self.getobject()

    def getverts(self):
        return XOctah.VERTS.copy() * self.size

    def getfaces(self):
        return XOctah.FACES.copy()

    def getedges(self):
        edges = set()
        for f in self.faces:
            for i in range(3):
                a = int(f[i])
                b = int(f[(i + 1) % 3])
                edges.add(tuple(sorted((a, b))))
        return np.array(sorted(edges), dtype=np.int32)

    def getobject(self):
        lines = ["o XOctah"]
        for v in self.verts:
            lines.append(f"v {v[0]} {v[1]} {v[2]}")
        for f in self.faces:
            lines.append(f"f {f[0]+1} {f[1]+1} {f[2]+1}")
        return "\n".join(lines) + "\n"