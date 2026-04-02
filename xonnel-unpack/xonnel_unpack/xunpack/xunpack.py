from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

from pathlib import Path

import zipfile
import py7zr
import tarfile


class XUnpack:
    def __init__(self, src:str|Path = None, tgt:str|Path=None):
        if src is None or tgt is None:
            raise ValueError("[ERROR] XUnpack.__init__() src and/or tgt can't be None")

        src, tgt = Path(src), Path(tgt)

        if not src.exists():
            raise ValueError(f"[ERROR] XUnpack.__init__() Source does not exist: {src}")

        if not src.is_file():
            raise ValueError(f"[ERROR] XUnpack.__init__() Source must be an archive file: {src}")

        tgt.mkdir(parents=True, exist_ok=True)

        name = src.name.lower()
        if name.endswith(".zip"):
            self._unpack_zip(src=src, tgt=tgt)
        elif name.endswith(".7z"):
            self._unpack_7z(src=src, tgt=tgt)
        elif name.endswith((".tar", ".tar.gz", ".tar.bz2", ".tar.xz")):
            self._unpack_tar(src=src, tgt=tgt)
        else:
            raise ValueError(f"[ERROR] XUnpack.__init__() Unsupported source extension: {src}")

    def _unpack_zip(self, src:Path=None, tgt:Path=None):
        with zipfile.ZipFile(src, "r") as archive:
            archive.extractall(tgt)

    def _unpack_7z(self, src:Path=None, tgt:Path=None):
        with py7zr.SevenZipFile(src, "r") as archive:
            archive.extractall(path=tgt)

    def _unpack_tar(self, src:Path=None, tgt:Path=None):
        with tarfile.open(src, "r:*") as archive:
            archive.extractall(tgt)














def test():
    srczip      = r"C:\CodeTest\XPackTest.zip"
    src7z       = r"C:\CodeTest\XPackTest.7z"
    srctargz    = r"C:\CodeTest\XPackTest.tar.gz"
    srctarbz2   = r"C:\CodeTest\XPackTest.tar.bz2"
    srctarxz    = r"C:\CodeTest\XPackTest.tar.xz"

    tgtzip      = r"C:\CodeTest\XUnpackTest_zip"
    tgt7z       = r"C:\CodeTest\XUnpackTest_7z"
    tgttargz    = r"C:\CodeTest\XUnpackTest_targz"
    tgttarbz2   = r"C:\CodeTest\XUnpackTest_tarbz2"
    tgttarxz    = r"C:\CodeTest\XUnpackTest_tarxz"

    XUnpack(src=srczip,    tgt=tgtzip)
    XUnpack(src=src7z,     tgt=tgt7z)
    XUnpack(src=srctargz,  tgt=tgttargz)
    XUnpack(src=srctarbz2, tgt=tgttarbz2)
    XUnpack(src=srctarxz,  tgt=tgttarxz)


if __name__ == "__main__":
    test()