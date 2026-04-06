from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

from pathlib import Path
import ctypes

import numpy as np
from numpy.ctypeslib import ndpointer


class XVoxel:
    DLL = None

    def __init__(self, array:np.ndarray=None, tres:float=1.0, size:tuple[float, float, float]=(1.0, 1.0, 1.0), origin:tuple[float, float, float]=(0.0, 0.0, 0.0)):
        self.array = np.ascontiguousarray(array, dtype=np.float32)
        self.tres = float(tres)
        self.size = tuple(map(float, size))
        self.origin = tuple(map(float, origin))

        if self.array.ndim != 3:
            raise ValueError("array must be 3d")

        self._dll()
        self._run()
        self._obj()

    @classmethod
    def _dll(cls):
        if cls.DLL is not None:
            return

        dll = ctypes.CDLL(str(Path(__file__).with_name("xvoxel.dll")))

        dll.xvoxel_create.argtypes = [ndpointer(dtype=np.float32, ndim=3, flags="C_CONTIGUOUS"), ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        dll.xvoxel_create.restype = ctypes.c_void_p

        dll.xvoxel_destroy.argtypes = [ctypes.c_void_p]
        dll.xvoxel_destroy.restype = None

        dll.xvoxel_vert_count.argtypes = [ctypes.c_void_p]
        dll.xvoxel_vert_count.restype = ctypes.c_size_t

        dll.xvoxel_face_count.argtypes = [ctypes.c_void_p]
        dll.xvoxel_face_count.restype = ctypes.c_size_t

        dll.xvoxel_edge_count.argtypes = [ctypes.c_void_p]
        dll.xvoxel_edge_count.restype = ctypes.c_size_t

        dll.xvoxel_copy_verts.argtypes = [ctypes.c_void_p, ndpointer(dtype=np.float32, ndim=2, flags="C_CONTIGUOUS")]
        dll.xvoxel_copy_verts.restype = None

        dll.xvoxel_copy_faces.argtypes = [ctypes.c_void_p, ndpointer(dtype=np.uint32, ndim=2, flags="C_CONTIGUOUS")]
        dll.xvoxel_copy_faces.restype = None

        dll.xvoxel_copy_edges.argtypes = [ctypes.c_void_p, ndpointer(dtype=np.uint32, ndim=2, flags="C_CONTIGUOUS")]
        dll.xvoxel_copy_edges.restype = None

        cls.DLL = dll

    def _run(self):
        dll = self.DLL

        d, h, w = self.array.shape
        sx, sy, sz = self.size
        ox, oy, oz = self.origin

        obj = dll.xvoxel_create(self.array, w, h, d, self.tres, sx, sy, sz, ox, oy, oz)
        if not obj:
            raise RuntimeError("xvoxel_create failed")

        try:
            nverts = dll.xvoxel_vert_count(obj)
            nfaces = dll.xvoxel_face_count(obj)
            nedges = dll.xvoxel_edge_count(obj)

            self.verts = np.empty((nverts, 3), dtype=np.float32)
            self.faces = np.empty((nfaces, 4), dtype=np.uint32)
            self.edges = np.empty((nedges, 2), dtype=np.uint32)

            if nverts: dll.xvoxel_copy_verts(obj, self.verts)
            if nfaces: dll.xvoxel_copy_faces(obj, self.faces)
            if nedges: dll.xvoxel_copy_edges(obj, self.edges)

        finally:
            dll.xvoxel_destroy(obj)

        zyx = np.argwhere(self.array >= self.tres)
        self.voxels = np.empty((0, 3), dtype=np.int32) if zyx.size == 0 else zyx[:, [2, 1, 0]].astype(np.int32, copy=False)

    def _obj(self):
        vs = self.verts.astype(str)
        fs = (self.faces + 1).astype(str)

        vs = "v " + vs[:, 0] + " " + vs[:, 1] + " " + vs[:, 2]
        fs = "f " + fs[:, 0] + " " + fs[:, 1] + " " + fs[:, 2] + " " + fs[:, 3]

        self.obj = "\n".join(np.concatenate([vs, fs]))