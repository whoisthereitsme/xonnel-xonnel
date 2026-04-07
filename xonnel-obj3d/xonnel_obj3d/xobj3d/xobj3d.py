from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...



from .xtetra    import XTetra
from .xcubic    import XCubic
from .xoctah    import XOctah
from .xicosa    import XIcosa  
from .xdodec    import XDodec
from .xsphere   import XSphere    






class XObj3d:
    def __init__(self, size:float=1.0):
        self.tetra:  XTetra  = XTetra(size=size)
        self.cubic:  XCubic  = XCubic(size=size)
        self.octah:  XOctah  = XOctah(size=size)
        self.icosa:  XIcosa  = XIcosa(size=size)
        self.dodec:  XDodec  = XDodec(size=size)
        self.sphere: XSphere = XSphere(size=size)



