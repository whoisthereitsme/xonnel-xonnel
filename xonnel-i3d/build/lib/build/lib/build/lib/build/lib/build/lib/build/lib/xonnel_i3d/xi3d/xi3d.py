# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
import xml.etree.ElementTree as ET
# [|] {-}
# [!] {-}




class XI3d:
    @classmethod
    def load(cls, path: str | Path = None):
        try:
            if path is None:
                print("[ERROR] [XI3d.load()] [Path cannot be None]")
                return None

            path = Path(path)
            tree = ET.parse(path)
            return tree.getroot()

        except FileNotFoundError as e:
            print(f"[ERROR] [XI3d.load()] [Error loading I3D from {path}: {e}]")
            return None

        except ET.ParseError as e:
            print(f"[ERROR] [XI3d.load()] [Error parsing I3D from {path}: {e}]")
            return None

        except Exception as e:
            print(f"[ERROR] [XI3d.load()] [Unexpected error loading I3D from {path}: {e}]")
            return None

    @classmethod
    def save(cls, path: str | Path = None, data=None, encoding: str = "utf-8", xml_declaration: bool = True):
        try:
            if path is None:
                print("[ERROR] [XI3d.save()] [Path cannot be None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            if data is None:
                print("[ERROR] [XI3d.save()] [Data cannot be None]")
                return False

            if isinstance(data, ET.ElementTree):
                tree = data
            elif isinstance(data, ET.Element):
                tree = ET.ElementTree(data)
            else:
                print("[ERROR] [XI3d.save()] [Data must be ET.Element or ET.ElementTree]")
                return False

            tree.write(path, encoding=encoding, xml_declaration=xml_declaration)
            return True

        except Exception as e:
            print(f"[ERROR] [XI3d.save()] [Error saving I3D to {path}: {e}]")
            return False
# [!] {-}