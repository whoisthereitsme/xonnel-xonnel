from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import numpy as np

from .xicosa import XIcosa


class XSphere(XIcosa):
    def __init__(self, size: float = 1.0, subs: int = 7):
        super().__init__(size=size)
        self.subs = int(subs)
        self.tiers = {}

        self.base_faces = self.faces.copy()
        self.base_normals = None

        self.divide()

    def divide(self):
        verts = self.verts.astype(np.float64).tolist()
        faces = self.faces.astype(np.int32).tolist()

        for i in range(self.subs):
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
            self.tiers[i] = np.array(faces, dtype=np.int32)

        self.verts = np.array(verts, dtype=np.float64)
        self.faces = np.array(faces, dtype=np.int32)
        self.edges = self.getedges()
        self.object = self.getobject()
        self.base_normals = self.getbasenormals()

    def getcenter(self, verts: list = None, cache: dict = None, p0: int = None, p1: int = None):
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

    def ll2xyz(self, lon: float = 0.0, lat: float = 0.0):
        lon = np.radians(lon)
        lat = np.radians(lat)

        x = self.size * np.cos(lat) * np.cos(lon)
        y = self.size * np.sin(lat)
        z = self.size * np.cos(lat) * np.sin(lon)

        return np.array([x, y, z], dtype=np.float64)

    def facecenter(self, face: np.ndarray = None):
        a, b, c = [self.verts[i] for i in face]
        center = (a + b + c) / 3.0
        norm = np.linalg.norm(center)
        if norm == 0:
            raise ValueError("Cannot normalize zero face center")
        return (center / norm) * self.size

    def getbasenormals(self):
        normals = []

        for face in self.base_faces:
            a, b, c = [self.verts[i] for i in face]
            fc = self.facecenter(face=face)

            n1 = np.cross(a, b)
            n2 = np.cross(b, c)
            n3 = np.cross(c, a)

            if np.dot(n1, fc) < 0:
                n1 = -n1
            if np.dot(n2, fc) < 0:
                n2 = -n2
            if np.dot(n3, fc) < 0:
                n3 = -n3

            normals.append((n1, n2, n3))

        return normals

    def intria(self, p: np.ndarray = None, face: np.ndarray = None, eps: float = 1e-12):
        a, b, c = [self.verts[i] for i in face]
        fc = self.facecenter(face=face)

        n1 = np.cross(a, b)
        n2 = np.cross(b, c)
        n3 = np.cross(c, a)

        if np.dot(n1, fc) < 0:
            n1 = -n1
        if np.dot(n2, fc) < 0:
            n2 = -n2
        if np.dot(n3, fc) < 0:
            n3 = -n3

        s1 = np.dot(n1, p)
        s2 = np.dot(n2, p)
        s3 = np.dot(n3, p)

        return (s1 >= -eps) and (s2 >= -eps) and (s3 >= -eps)

    def intriabase(self, p: np.ndarray = None, faceidx: int = 0, eps: float = 1e-12):
        n1, n2, n3 = self.base_normals[faceidx]

        s1 = np.dot(n1, p)
        s2 = np.dot(n2, p)
        s3 = np.dot(n3, p)

        return (s1 >= -eps) and (s2 >= -eps) and (s3 >= -eps)

    def facedistsum(self, p: np.ndarray = None, face: np.ndarray = None):
        a, b, c = [self.verts[i] for i in face]
        return (
            np.linalg.norm(p - a)
            + np.linalg.norm(p - b)
            + np.linalg.norm(p - c)
        )

    def find(self, lon: float = 0.0, lat: float = 0.0):
        p = self.ll2xyz(lon=lon, lat=lat)

        # STEP 1: exact base-face lookup (fast exact, precomputed normals)
        parent_idx = None
        parent_face = None

        for i, face in enumerate(self.base_faces):
            if self.intriabase(p=p, faceidx=i):
                parent_idx = i
                parent_face = face
                break

        if parent_idx is None:
            raise ValueError(f"No base triangle found for lon={lon}, lat={lat}")

        result = {
            "tier": -1,
            "index": int(parent_idx),
            "face": np.array(parent_face, dtype=np.int32),
            "verts": self.verts[np.array(parent_face, dtype=np.int32)],
            "point": p,
        }

        # STEP 2: fast child descent by smallest distance-sum
        for tier in range(self.subs):
            faces = self.tiers[tier]

            start = parent_idx * 4
            stop = start + 4

            best_idx = None
            best_face = None
            best_dist = None

            for child_idx in range(start, stop):
                face = faces[child_idx]
                dist = self.facedistsum(p=p, face=face)

                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_idx = child_idx
                    best_face = face

            if best_face is None:
                raise ValueError(
                    f"No child triangle found at tier={tier} for lon={lon}, lat={lat}"
                )

            parent_idx = best_idx
            parent_face = best_face

            result = {
                "tier": tier,
                "index": int(parent_idx),
                "face": np.array(parent_face, dtype=np.int32),
                "verts": self.verts[np.array(parent_face, dtype=np.int32)],
                "point": p,
            }

        return result