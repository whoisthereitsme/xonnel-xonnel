# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
import json

# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XJson:
    @classmethod
    def load(cls, path:str|Path=None):
        try:
            if path is None:
                print("[ERROR] [XJson.load()] [Path cannot be None]")
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] [XJson.load()] [Error loading JSON from {path}: {e}]")
            return None

    
    @classmethod
    def save(cls, path:str|Path=None, data:dict=None, indent:int=4):
        try:
            if path is None:
                print("[ERROR] [XJson.save()] [Path cannot be None]")
                return False
            with open(path, "w") as f:
                json.dump(data, f, indent=indent)
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR] [XJson.save()] [Error saving JSON to {path}: {e}]")
            return False


# [!] {-}



