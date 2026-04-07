from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xicosa import XIcosa


class XSphere(XIcosa):
    def __init__(self, size:float=1.0, subs:int=5):
        super().__init__(size=size)
        self.subs = subs
        self.subdivide()

    def subdivide(self):
        verts = self.verts.astype(np.float64).tolist()
        faces = self.faces.astype(np.int32).tolist()

        for _ in range(self.subs):
            edge_cache = {}
            new_faces = []

            for face in faces:
                a, b, c = face

                ab = self.getcenter(verts=verts, cache=edge_cache, p0=a, p1=b)
                bc = self.getcenter(verts=verts, cache=edge_cache, p0=b, p1=c)
                ca = self.getcenter(verts=verts, cache=edge_cache, p0=c, p1=a)

                new_faces.extend([
                    (a, ab, ca),
                    (b, bc, ab),
                    (c, ca, bc),
                    (ab, bc, ca),
                ])

            faces = new_faces

        self.verts = np.array(verts, dtype=np.float64)
        self.faces = np.array(faces, dtype=np.int32)
        self.edges = self.getedges()
        self.object = self.getobject()

    def getcenter(self, verts:list=None, cache:dict=None, p0:int=None, p1:int=None):
        edge = tuple(sorted((int(p0), int(p1))))

        if edge in cache:
            return cache[edge]

        v0 = np.array(verts[p0], dtype=np.float64)
        v1 = np.array(verts[p1], dtype=np.float64)

        center = (v0 + v1) / 2.0
        norm = np.linalg.norm(center)

        if norm == 0:
            raise ValueError(f"Cannot normalize midpoint of edge {edge}")

        center = (center / norm) * self.size

        idx = len(verts)
        verts.append(center.tolist())
        cache[edge] = idx
        return idx