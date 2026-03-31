# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XTxt:
    @classmethod
    def load(cls, path: str | Path = None, encoding: str = "utf-8"):
        try:
            if path is None:
                print("[ERROR] [XTxt.load()] [Path cannot be None]")
                return None

            path = Path(path)
            with open(path, "r", encoding=encoding) as f:
                return f.read()

        except FileNotFoundError as e:
            print(f"[ERROR] [XTxt.load()] [Error loading TXT from {path}: {e}]")
            return None

        except Exception as e:
            print(f"[ERROR] [XTxt.load()] [Unexpected error loading TXT from {path}: {e}]")
            return None

    @classmethod
    def save(cls, path: str | Path = None, data: str = None, encoding: str = "utf-8"):
        try:
            if path is None:
                print("[ERROR] [XTxt.save()] [Path cannot be None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            if data is None:
                data = ""

            with open(path, "w", encoding=encoding) as f:
                f.write(str(data))

            return True

        except Exception as e:
            print(f"[ERROR] [XTxt.save()] [Error saving TXT to {path}: {e}]")
            return False

# [!] {-}