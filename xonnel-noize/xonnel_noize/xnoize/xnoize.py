from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...




import time
from math import sin, cos, tan, pi

class Noize:
    BASE = {
        "PERLIN": dll("perlin.dll"),
        "SIMPLEX": dll("simplex.dll"),
        "WORLEY": dll("worley.dll")
    }

    POST = {
        "FLIP":         lambda noize=None, weight=1.0: (weight * (1-noize)),
        "INV":          lambda noize=None, weight=1.0: (weight * (1/noize)),
        "NEG":          lambda noize=None, weight=1.0: (weight * -noize),
        "POS":          lambda noize=None, weight=1.0: (weight *  noize),
        "POW":          lambda noize=None, weight=1.0: (weight *  noize**2),
        "EXP":          lambda noize=None, weight=1.0: (weight *  2**noize),
        "ABS":          lambda noize=None, weight=1.0: (weight *  abs(noize)),
        "SIN":          lambda noize=None, weight=1.0: (weight *  sin(noize)),
        "COS":          lambda noize=None, weight=1.0: (weight *  cos(noize)),
        "TAN":          lambda noize=None, weight=1.0: (weight *  tan(noize)),
        "INVPOW":       lambda noize=None, weight=1.0: (weight *  1/(noize**2)),
        "INVEXP":       lambda noize=None, weight=1.0: (weight *  1/(2**noize)),
        "INVSIN":       lambda noize=None, weight=1.0: (weight *  1/sin(noize)),
        "INVCOS":       lambda noize=None, weight=1.0: (weight *  1/cos(noize)),
        "INVTAN":       lambda noize=None, weight=1.0: (weight *  1/tan(noize)),
    }


    def __init__(self, size:int|tuple[int]=None, repeat:int|tuple[int]=None, offset:float|tuple[float]=None, scale:float|tuple[float]=None, octs:int=None, pers:float=None, lacu:float=None, seed:int=None, perlin:float=None, simplex:float=None, worley:float=None, post:list[str]=None, norm:tuple=None):
        self.size:tuple   = self.get3d(value=size,   fill=1)
        self.repeat:tuple = self.get3d(value=repeat, fill=2**16-1)
        self.offset:tuple = self.get3d(value=offset, fill=0.0)
        self.scale:tuple  = self.get3d(value=scale,  fill=1.0)
        self.octs:int     = self.getocts(octs=octs)
        self.pers:float   = self.getpers(pers=pers)
        self.lacu:float   = self.getlacu(lacu=lacu)
        self.seed:int     = self.getseed(seed=seed)

        self.weight:dict  = self.getweight(perlin=perlin, simplex=simplex, worley=worley)
        self.post:list    = self.getpost(post=post)
        self.norm:tuple   = self.getnorm(norm=norm)

    def getweight(self, perlin:float=None, simplex:float=None, worley:float=None):
        perlin  = 0.0 if perlin  is None else perlin
        simplex = 0.0 if simplex is None else simplex
        worley  = 0.0 if worley  is None else worley
        total = perlin + simplex + worley
        if total == 0.0:
            return {"PERLIN": 1.0, "SIMPLEX": None, "WORLEY": None}
        return {
            "PERLIN":  perlin  / total,
            "SIMPLEX": simplex / total,
            "WORLEY":  worley  / total
        }

    def getseed(self, seed:int=None):
        if seed is None:
            return int(time.time())
        return seed
    
    def getpost(self, post:list[str]=None):
        if post is None:
            return []
        return [Noize.POST.get(p.upper(), lambda noize=None: noize) for p in post]
    
    def getocts(self, octs:int=None):
        if octs is None:
            return 1
        else:
            return int(octs)
        
    def getpers(self, pers:float=None):
        if pers is None:
            return 0.5
        else:
            return float(pers)
        
    def getlacu(self, lacu:float=None):
        if lacu is None:
            return 2.0
        else:
            return float(lacu)
        
    def getnorm(self, norm:tuple=None):
        if norm is None:
            return (0.0, 1.0)
        else:
            return tuple(norm)

    def get3d(self, value:float|int|tuple[int]=None, fill=1):
        if value is None:
            return (fill,        fill,        fill)
        if isinstance(value, int):
            return (value,       fill,        fill)
        if len(value) == 1:
            return (value[0],    fill,        fill)
        if len(value) == 2:
            return (value[0],    value[1],    fill)
        if len(value) == 3:
            return value
        raise ValueError(f"Invalid value for get3d: {value}")
        



class XNoize:
    DLL = None  

    def __init__(self, cfg:Noize=None):
        self.cfg = cfg

        self.init()

    def init(self):
        if self.cfg is None:
            self.cfg = Noize()

        self.PNOIZE = self.getpnoize()
        self.SNOIZE = self.getsnoize()
        self.WNOIZE = self.getwnoize()
        self.RNOIZE = self.getrnoize()