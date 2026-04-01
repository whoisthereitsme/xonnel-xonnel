from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    ...






from pathlib import Path
import pickle






class XPkl:
    @classmethod
    def save(cls, data:Any=None, path:str|Path=None):
        if path is None:
            raise ValueError("[ERROR] XPkl.save() No path provided for saving data.")
        
        with open(Path(path), 'wb') as file:
            pickle.dump(data, file)
        
    @classmethod
    def load(cls, path:str|Path=None):
        if path is None:
            raise ValueError("[ERROR] XPkl.load() No path provided for loading data.")
        
        with open(Path(path), 'rb') as file:
            data = pickle.load(file)
        
        return data
