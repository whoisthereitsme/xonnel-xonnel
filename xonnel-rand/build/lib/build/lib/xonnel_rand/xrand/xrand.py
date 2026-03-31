import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...





import random
import time
import uuid







class XRand:

    CHARSLOWER      = "abcdefghijklmnopqrstuvwxyz"
    CHARSUPPER      = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    CHARSNUMBERS    = "0123456789"
    CHARSSYMBOLS    = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"


    @classmethod
    def seed(cls, seed=None):
        random.seed(seed)

    @classmethod
    def shuffle(cls, seq:dict|list|tuple|str=None):
        if isinstance(seq, str):
            seq = list(seq)
            random.shuffle(seq)
            return ''.join(seq)
        
        elif isinstance(seq, list):
            random.shuffle(seq)
            return seq
        
        elif isinstance(seq, tuple):
            seq = list(seq)
            random.shuffle(seq)
            return tuple(seq)
        
        elif isinstance(seq, dict):
            items = list(seq.items())
            random.shuffle(items)
            return dict(items)
        
        else:
            raise ValueError(f"[ERROR] XRand.shuffle() Unsupported sequence type for shuffle: {type(seq)}")
    
    @classmethod
    def sample(cls, seq:dict|list|tuple|str=None, k:int=1):
        data, typ = cls._seq(seq)
        result = random.sample(data, k)
        return cls._wrap(typ=typ, data=result)

    @classmethod
    def choice(cls, seq:dict|list|tuple|str=None):
        data, _ = cls._seq(seq)
        return random.choice(data)

    @classmethod
    def choices(cls, seq:list|tuple|str=None, k:int=1):
        if isinstance(seq, dict):
            raise ValueError(f"[ERROR] XRand.choices() Cannot use dict as sequence for choices()\nREASON: It cannot guarantee len(dict) == k because duplicates would be overwritten")
        
        data, typ = cls._seq(seq)
        result = random.choices(data, k=k)
        return cls._wrap(typ=typ, data=result)
    
    @classmethod
    def bytes(cls, n:int=16):
        return random.randbytes(n)
    
    @classmethod
    def rand(cls):
        return random.random()
    
    @classmethod
    def range(cls, low:int=0, high:int=1, step:int=1):   
        return random.randrange(low, high, step)
    
    @classmethod
    def int(cls, low:int=0, high:int=1) -> int:
        low, high = cls._order(low=low, high=high)
        return random.randint(low, high)
    
    @classmethod
    def float(cls, low:float=0.0, high:float=1.0) -> float:
        low, high = cls._order(low=low, high=high)
        return random.uniform(low, high)
    
    @classmethod
    def bool(cls, chance:float=0.5):
        return random.random() < chance
    
    @classmethod
    def str(cls, length:int=8, chars:str=None, numbers:bool=True, uppercase:bool=True, lowercase:bool=True, symbols:bool=False):
        if chars is None:
            chars = ""
            if lowercase:
                chars += cls.CHARSLOWER
            if uppercase:
                chars += cls.CHARSUPPER
            if numbers:
                chars += cls.CHARSNUMBERS
            if symbols:
                chars += cls.CHARSSYMBOLS

        if chars == "" and length > 0:
            raise ValueError("[ERROR] XRand.str() No characters available to generate string.\nlength of result cannot be matched with no characters.\nPlease enable at least one of lowercase, uppercase, numbers, symbols or provide a custom chars string.")
        return ''.join(random.choices(chars, k=length))    

    @classmethod
    def uuid(cls):
        return str(uuid.uuid4())
    
    @classmethod
    def _order(cls, low:int=0, high:int=1):
        if low > high:
            low, high = high, low
        return low, high
    
    @classmethod
    def _seq(cls, seq=None):
        if isinstance(seq, dict):
            return list(seq.items()), dict
        elif isinstance(seq, str):
            return list(seq), str
        elif isinstance(seq, list):
            return seq, list
        elif isinstance(seq, tuple):
            return list(seq), tuple
        else:
            raise ValueError(f"[ERROR] XRand._seq() Unsupported sequence type: {type(seq)}")
        
    @classmethod
    def _wrap(cls, typ=None, data=None):
        if typ is str:
            return ''.join(data)
        if typ in (dict, list, tuple):
            return typ(data)
       
        raise ValueError(f"[ERROR] XRand._wrap() Unsupported type for: {typ}")

    """
    DISTRIBUTIONS
    """
    @classmethod
    def gauss(cls, low=0, high=100, mu=None, sigma=None):
        low, high = cls._order(low=low, high=high)
        if mu is None:
            mu = (low + high) / 2
        if sigma is None:
            sigma = (high - low) / 6
        v = random.gauss(mu, sigma)
        return max(low, min(high, v))

    @classmethod
    def tria(cls, low=0, high=100, mu=None):
        low, high = cls._order(low=low, high=high)
        if mu is None:
            mu = (low + high) / 2
        return random.triangular(low, high, mu)

    @classmethod
    def exp(cls, low=0, high=100, lambd=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.expovariate(lambd)
        v_norm = 1 - math.exp(-lambd * v)
        return low + (high - low) * v_norm
        




    @classmethod
    def weibull(cls, low=0, high=100, alpha=1.0, beta=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.weibullvariate(alpha, beta)
        v_norm = 1 - math.exp(-((v / alpha) ** beta))
        return low + (high - low) * v_norm

    @classmethod
    def beta(cls, low=0, high=100, alpha=1.0, beta=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.betavariate(alpha, beta)   # 0..1
        return low + (high - low) * v
    
    @classmethod
    def gamma(cls, low=0, high=100, alpha=1.0, beta=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.gammavariate(alpha, beta)
        v_norm = v / (v + 1)   # smooth squash
        return low + (high - low) * v_norm
        
    @classmethod
    def vonmises(cls, low=0, high=100, mu=0.0, kappa=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.vonmisesvariate(mu, kappa)  # 0..2π
        v_norm = v / (2 * math.pi)
        return low + (high - low) * v_norm

    @classmethod
    def pareto(cls, low=0, high=100, alpha=1.0):
        low, high = cls._order(low=low, high=high)
        v = random.paretovariate(alpha)  # ≥1
        v = v - 1
        v_norm = 1 - (1 / v) ** alpha
        return low + (high - low) * v_norm
    
    @classmethod
    def sine(cls, low=0, high=100, phase=None, freq=1.0):
        low, high = cls._order(low=low, high=high)
        if phase is None:
            phase = random.random() * 2 * math.pi
        x = random.random() * 2 * math.pi * freq
        v = math.sin(x + phase)
        v_norm = (v + 1) / 2
        return low + (high - low) * v_norm
            



XRand.seed(int(time.time()))




