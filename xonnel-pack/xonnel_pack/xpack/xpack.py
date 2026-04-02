from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

from pathlib import Path

import zipfile
import py7zr
import tarfile


class XPack:
    def __init__(self, src:str|Path=None, tgt:str|Path=None):
        if src is None or tgt is None:
            raise ValueError("[ERROR] XPack.__init__() src and/or tgt can't be None")

        src, tgt = Path(src), Path(tgt)

        if not src.exists():
            raise ValueError(f"[ERROR] XPack.__init__() Source does not exist: {src}")

        name = tgt.name.lower()

        if name.endswith(".zip"):
            self._pack_to_zip(src=src, tgt=tgt)
        elif name.endswith(".7z"):
            self._pack_to_7z(src=src, tgt=tgt)
        elif name.endswith((".tar", ".tar.gz", ".tar.bz2", ".tar.xz")):
            self._pack_to_tar(src=src, tgt=tgt)
        else:
            raise ValueError(f"[ERROR] XPack.__init__() Unsupported target extension: {tgt}")

    def _pack_to_zip(self, src:Path=None, tgt:Path=None):
        with zipfile.ZipFile(tgt, "w", zipfile.ZIP_DEFLATED) as archive:
            if src.is_file():
                archive.write(src, arcname=src.name)
            elif src.is_dir():
                for path in src.rglob("*"):
                    archive.write(path, arcname=path.relative_to(src))

    def _pack_to_7z(self, src:Path=None, tgt:Path=None):
        with py7zr.SevenZipFile(tgt, "w") as archive:
            if src.is_file():
                archive.write(src, arcname=src.name)
            elif src.is_dir():
                for path in src.rglob("*"):
                    archive.write(path, arcname=str(path.relative_to(src)))

    def _pack_to_tar(self, src:Path=None, tgt:Path=None):
        name = tgt.name.lower()

        if name.endswith(".tar"):
            mode = "w"
        elif name.endswith(".tar.gz"):
            mode = "w:gz"
        elif name.endswith(".tar.bz2"):
            mode = "w:bz2"
        elif name.endswith(".tar.xz"):
            mode = "w:xz"
        else:
            raise ValueError(f"[ERROR] XPack._pack_to_tar() Unsupported tar extension: {name}")

        with tarfile.open(tgt, mode) as archive:
            if src.is_file():
                archive.add(src, arcname=src.name)
            elif src.is_dir():
                for path in src.rglob("*"):
                    archive.add(path, arcname=str(path.relative_to(src)))





def test():
    src         = r"C:\CodeTest\XPackTest"
    tgtzip      = r"C:\CodeTest\XPackTest.zip"
    tgt7z       = r"C:\CodeTest\XPackTest.7z"
    tgttargz    = r"C:\CodeTest\XPackTest.tar.gz"
    tgttarbz2   = r"C:\CodeTest\XPackTest.tar.bz2"
    tgttarxz    = r"C:\CodeTest\XPackTest.tar.xz"

    XPack(src=src, tgt=tgtzip)
    XPack(src=src, tgt=tgttargz)
    XPack(src=src, tgt=tgttarbz2)
    XPack(src=src, tgt=tgttarxz)
    XPack(src=src, tgt=tgt7z)


if __name__ == "__main__":
    test()