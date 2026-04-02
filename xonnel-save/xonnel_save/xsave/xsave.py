from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...











import json
import pickle
import xml.etree.ElementTree as ET





from pathlib import Path
from PIL import Image











class XSave:
    def __new__(cls, path:str|Path=None, data=None, force:str=None):
        if path is None:
            raise ValueError("[ERROR] XSave.__new__() path cannot be None")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        return cls._save(path=path, data=data, force=force)

    @classmethod
    def _save(cls, path:Path=None, data=None, force:str=None):
        if force is not None:
            force = force.lower().strip()

            if force == "txt":
                return cls._save_as_txt(path=path, data=data)
            elif force == "json":
                return cls._save_as_json(path=path, data=data)
            elif force == "xml":
                return cls._save_as_xml(path=path, data=data)
            elif force == "pkl":
                return cls._save_as_pkl(path=path, data=data)
            elif force == "img":
                return cls._save_as_img(path=path, data=data)
            elif force == "bin":
                return cls._save_as_bin(path=path, data=data)
            else:
                raise ValueError(f"[ERROR] XSave._save() Unsupported force mode: {force}")

        ext = path.suffix.lower()

        if ext in (".txt", ".log", ".py", ".lua", ".md", ".html", ".htm", ".css"):
            return cls._save_as_txt(path=path, data=data)

        elif ext in (".json",):
            return cls._save_as_json(path=path, data=data)

        elif ext in (".xml", ".i3d"):
            return cls._save_as_xml(path=path, data=data)

        elif ext in (".pkl", ".pickle"):
            return cls._save_as_pkl(path=path, data=data)

        elif ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
            return cls._save_as_img(path=path, data=data)

        else:
            return cls._save_as_bin(path=path, data=data)

    @classmethod
    def _save_as_txt(cls, path:Path=None, data=None):
        if data is None:
            data = ""
        if not isinstance(data, str):
            data = str(data)

        with path.open("w", encoding="utf-8") as f:
            f.write(data)

        return path

    @classmethod
    def _save_as_json(cls, path:Path=None, data=None):
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return path

    @classmethod
    def _save_as_xml(cls, path:Path=None, data=None):
        if isinstance(data, ET.ElementTree):
            tree = data
        elif isinstance(data, ET.Element):
            tree = ET.ElementTree(data)
        else:
            raise ValueError("[ERROR] XSave._save_as_xml() data must be ET.ElementTree or ET.Element")

        tree.write(path, encoding="utf-8", xml_declaration=True)

        return path

    @classmethod
    def _save_as_pkl(cls, path:Path=None, data=None):
        with path.open("wb") as f:
            pickle.dump(data, f)

        return path

    @classmethod
    def _save_as_img(cls, path:Path=None, data=None):
        if not isinstance(data, Image.Image):
            raise ValueError("[ERROR] XSave._save_as_img() data must be PIL.Image.Image")

        data.save(path)

        return path

    @classmethod
    def _save_as_bin(cls, path:Path=None, data=None):
        if data is None:
            data = b""

        if isinstance(data, bytearray):
            data = bytes(data)

        if not isinstance(data, bytes):
            raise ValueError("[ERROR] XSave._save_as_bin() data must be bytes or bytearray")

        with path.open("wb") as f:
            f.write(data)

        return path












