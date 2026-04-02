from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...

import json
import pickle
import xml.etree.ElementTree as ET

from pathlib import Path
from PIL import Image


class XLoad:
    def __new__(cls, path:str|Path=None, force:str=None):
        if path is None:
            raise ValueError("[ERROR] XLoad.__new__() path cannot be None")

        path = Path(path)

        if not path.exists():
            raise ValueError(f"[ERROR] XLoad.__new__() Source does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"[ERROR] XLoad.__new__() Source must be a file: {path}")

        return cls._load(path=path, force=force)

    @classmethod
    def _load(cls, path:Path=None, force:str=None):
        if force is not None:
            force = force.lower().strip()

            if force == "txt":
                return cls._load_as_txt(path=path)
            elif force == "json":
                return cls._load_as_json(path=path)
            elif force == "xml":
                return cls._load_as_xml(path=path)
            elif force == "pkl":
                return cls._load_as_pkl(path=path)
            elif force == "img":
                return cls._load_as_img(path=path)
            elif force == "bin":
                return cls._load_as_bin(path=path)
            else:
                raise ValueError(f"[ERROR] XLoad._load() Unsupported force mode: {force}")

        ext = path.suffix.lower()

        if ext in (".txt", ".log", ".py", ".lua", ".md", ".html", ".htm", ".css"):
            return cls._load_as_txt(path=path)

        elif ext in (".json",):
            return cls._load_as_json(path=path)

        elif ext in (".xml", ".i3d"):
            return cls._load_as_xml(path=path)

        elif ext in (".pkl", ".pickle"):
            return cls._load_as_pkl(path=path)

        elif ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
            return cls._load_as_img(path=path)

        else:
            return cls._load_as_bin(path=path)

    @classmethod
    def _load_as_txt(cls, path:Path=None):
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def _load_as_json(cls, path:Path=None):
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _load_as_xml(cls, path:Path=None):
        return ET.parse(path)

    @classmethod
    def _load_as_pkl(cls, path:Path=None):
        with path.open("rb") as f:
            return pickle.load(f)

    @classmethod
    def _load_as_img(cls, path:Path=None):
        return Image.open(path)

    @classmethod
    def _load_as_bin(cls, path:Path=None):
        with path.open("rb") as f:
            return f.read()












def test():
    paths = [
        r"C:\CodeTest\test.txt",
        r"C:\CodeTest\test.json",
        r"C:\CodeTest\test.xml",
        r"C:\CodeTest\test.html",
        r"C:\CodeTest\test.css",
        r"C:\CodeTest\test.pkl",
        r"C:\CodeTest\test.png",
        r"C:\CodeTest\test.bin",
    ]

    for path in paths:
        try:
            data = XLoad(path)
            print(f"{path} -> {type(data)}")
        except Exception as e:
            print(f"[ERROR] {path} -> {e}")

    print()
    print("FORCED MODES")
    print(XLoad(r"C:\CodeTest\test.json", force="txt"))
    print(type(XLoad(r"C:\CodeTest\test.xml", force="bin")))
    print(type(XLoad(r"C:\CodeTest\test.txt", force="bin")))


if __name__ == "__main__":
    test()