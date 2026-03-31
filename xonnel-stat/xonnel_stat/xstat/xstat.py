from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...









import statistics as stats
import numpy as np

from typing import Any
from scipy import stats as scipy_stats









class XStat:
    @classmethod
    def _cast(cls, data:Any=None) -> np.ndarray:
        if data is None:
            raise ValueError("[ERROR] XStat._cast() data cannot be None")
        if isinstance(data, dict):
            data = list(data.values())
        arr = np.asarray(list(data) if not isinstance(data, (list, tuple, np.ndarray)) else data, dtype=float)
        if arr.ndim != 1:
            arr = arr.ravel()
        if arr.size == 0:
            raise ValueError("[ERROR] XStat._cast() data cannot be empty")

        return arr

    @classmethod
    def _cast2(cls, x:Any=None, y:Any=None) -> tuple[np.ndarray, np.ndarray]:
        if isinstance(x, dict) and isinstance(y, dict):
            keys = [k for k in x if k in y]
            if not keys:
                raise ValueError("[ERROR] XStat._cast2() x and y dicts have no overlapping keys")
            xa = np.asarray([x[k] for k in keys], dtype=float)
            ya = np.asarray([y[k] for k in keys], dtype=float)
        else:
            xa = cls._cast(data=x)
            ya = cls._cast(data=y)

        if xa.size != ya.size:
            raise ValueError("[ERROR] XStat._cast2() x and y must have same length")
        if xa.size == 0:
            raise ValueError("[ERROR] XStat._cast2() x and y cannot be empty")
        return xa, ya

    # basics
    @classmethod
    def count(cls, data:Any=None) -> int:
        return int(cls._cast(data=data).size)

    @classmethod
    def sum(cls, data:Any=None) -> float:
        return float(np.sum(cls._cast(data=data)))

    @classmethod
    def mean(cls, data:Any=None) -> float:
        return float(stats.mean(cls._cast(data=data)))

    @classmethod
    def median(cls, data:Any=None) -> float:
        return float(stats.median(cls._cast(data=data)))

    @classmethod
    def min(cls, data:Any=None) -> float:
        return float(np.min(cls._cast(data=data)))

    @classmethod
    def max(cls, data:Any=None) -> float:
        return float(np.max(cls._cast(data=data)))

    @classmethod
    def minmax(cls, data:Any=None) -> tuple[float, float]:
        a = cls._cast(data=data)
        return float(np.min(a)), float(np.max(a))

    # positional
    @classmethod
    def percentile(cls, data:Any=None, p:float=None) -> float:
        return float(np.percentile(cls._cast(data=data), p))

    @classmethod
    def percentiles(cls, data:Any=None, ps:Any=None) -> dict[float, float]:
        if isinstance(ps, dict):
            ps = list(ps.values())
        vals = np.percentile(cls._cast(data=data), ps)
        return {float(p): float(v) for p, v in zip(ps, vals)}

    # spread
    @classmethod
    def variance(cls, data:Any=None, sample:bool=True) -> float:
        a = cls._cast(data=data)
        if sample:
            return float(stats.variance(a))
        return float(stats.pvariance(a))

    @classmethod
    def std(cls, data:Any=None, sample:bool=True) -> float:
        a = cls._cast(data=data)
        if sample:
            return float(stats.stdev(a))
        return float(stats.pstdev(a))

    # shape
    @classmethod
    def skewness(cls, data:Any=None, bias:bool=False) -> float:
        return float(scipy_stats.skew(cls._cast(data=data), bias=bias))

    @classmethod
    def kurtosis(cls, data:Any=None, fisher:bool=True, bias:bool=False) -> float:
        return float(scipy_stats.kurtosis(cls._cast(data=data), fisher=fisher, bias=bias))

    # relationships
    @classmethod
    def correlation(cls, x:Any=None, y:Any=None) -> float:
        xa, ya = cls._cast2(x=x, y=y)
        return float(stats.correlation(xa, ya))

    @classmethod
    def regression(cls, x:Any=None, y:Any=None) -> dict[str, float]:
        xa, ya = cls._cast2(x=x, y=y)
        r = scipy_stats.linregress(xa, ya)
        return {
            "slope": float(r.slope),
            "intercept": float(r.intercept),
            "rvalue": float(r.rvalue),
            "pvalue": float(r.pvalue),
            "stderr": float(r.stderr),
            "intercept_stderr": float(r.intercept_stderr),
        }
    
    @classmethod
    def _clip(cls, data:int|float=None, low:float=0, high:float=100) -> float:
        return min(max(float(data), low), high)

    @classmethod
    def between(cls, data:Any=None, p0:int=0, p1:int=100) -> list[float]:
        p0 = cls._clip(data=p0, low=0, high=100)
        p1 = cls._clip(data=p1, low=0, high=100)
        if p0 > p1: p0, p1 = p1, p0
        a = np.sort(cls._cast(data=data))
        v0 = np.percentile(a, p0)
        v1 = np.percentile(a, p1)
        return a[(a >= v0) & (a <= v1)].tolist()










