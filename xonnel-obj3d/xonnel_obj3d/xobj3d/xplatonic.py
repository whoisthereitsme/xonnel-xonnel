



class XPlatonic:
    def __init__(self, size:float=1.0):
        self.size = float(size)
        

    def getverts(self):
        raise NotImplementedError("XPlatonic.getverts() must be implemented by subclasses")
    
    def getfaces(self):
        raise NotImplementedError("XPlatonic.getfaces() must be implemented by subclasses")
    
    def getedges(self):
        raise NotImplementedError("XPlatonic.getedges() must be implemented by subclasses")
    
    def getobject(self):
        raise NotImplementedError("XPlatonic.getobject() must be implemented by subclasses")
