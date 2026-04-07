from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xplatonic import XPlatonic


PHI = (1.0 + np.sqrt(5.0)) / 2.0


class XIcosa(XPlatonic):
    VERTS = np.array([
        (-1,  PHI,  0),
        ( 1,  PHI,  0),
        (-1, -PHI,  0),
        ( 1, -PHI,  0),
        ( 0, -1,  PHI),
        ( 0,  1,  PHI),
        ( 0, -1, -PHI),
        ( 0,  1, -PHI),
        ( PHI,  0, -1),
        ( PHI,  0,  1),
        (-PHI,  0, -1),
        (-PHI,  0,  1),
    ], dtype=np.float64)

    FACES = np.array([
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
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
        norms = np.linalg.norm(XIcosa.VERTS, axis=1, keepdims=True)
        return (XIcosa.VERTS / norms) * self.size

    def getfaces(self):
        return XIcosa.FACES.copy()

    def getedges(self):
        edges = set()
        for f in self.faces:
            for i in range(3):
                a = int(f[i])
                b = int(f[(i + 1) % 3])
                edges.add(tuple(sorted((a, b))))
        return np.array(sorted(edges), dtype=np.int32)

    def getobject(self):
        lines = ["o XIcosa"]
        for v in self.verts:
            lines.append(f"v {v[0]} {v[1]} {v[2]}")
        for f in self.faces:
            lines.append(f"f {f[0]+1} {f[1]+1} {f[2]+1}")
        return "\n".join(lines) + "\n"