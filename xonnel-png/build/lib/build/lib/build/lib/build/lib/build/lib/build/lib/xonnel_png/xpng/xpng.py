# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
from PIL import Image
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XPng:
    @classmethod
    def load(cls, path: str | Path = None):
        try:
            if path is None:
                print("[ERROR] [XPng.load()] [Path cannot be None]")
                return None

            path = Path(path)
            img = Image.open(path)
            return img.copy()  # detach from file handle

        except FileNotFoundError as e:
            print(f"[ERROR] [XPng.load()] [Error loading PNG from {path}: {e}]")
            return None

        except Exception as e:
            print(f"[ERROR] [XPng.load()] [Unexpected error loading PNG from {path}: {e}]")
            return None

    @classmethod
    def save(cls, path: str | Path = None, data: Image.Image = None):
        try:
            if path is None:
                print("[ERROR] [XPng.save()] [Path cannot be None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            if data is None:
                print("[ERROR] [XPng.save()] [Data cannot be None]")
                return False

            if not isinstance(data, Image.Image):
                print(f"[ERROR] [XPng.save()] [Data must be PIL.Image.Image, got {type(data).__name__}]")
                return False

            data.save(path, format="PNG")
            return True

        except Exception as e:
            print(f"[ERROR] [XPng.save()] [Error saving PNG to {path}: {e}]")
            return False

# [!] {-}