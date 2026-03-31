# [!] {+} IMPORTS
from typing import TYPE_CHECKING

# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...

# [|] {-}





# [|] {+} IMPORTS 3RD PARTY
...

# [|] {-}





# [|] {+} IMPORTS MYMODULES
...

# [|] {-}





# [!] {-}







# [!] {+} GLOBALS
# [|] {+} GLOBAL CONSTANTS
...

# [|] {-}





# [|] {+} GLOBAL VARIABLES
...

# [|] {-}





# [|] {+} GLOBAL ALIASES
...

# [|] {-}





# [|] {+} GLOBAL FUNCTIONS
def global_function1():
    ...
    return ...

# [|] {-}





# [!] {-}







# [!] {+} CLASSES
class XGui:
    # [|] {+} ATTRIBUTES
    ...

    # [|] {-}





    # [|] {+} INITIALIZING METHODS
    def __init__(self):
        self.init()
        self.post()
        ...


    def init(self):
        ...

    def post(self):
        ...

    # [|] {-}





    # [|] {+} NORMAL METHODS
    def method1(self):
        ...
        return ...

    # [|] {-}





    # [|] {+} PUBLIC METHODS
    def getdata(self):
        data = None
        return data

    # [|] {-}





    # [|] {+} DUNDER METHODS
    def __repr__(self):
        return f"<{self.__class__.__name__}()>"

    # [|] {-}





# [!] {-}







# [!] {+} SPECIALS
def main():
    ...
    return ...

def test():
    ...
    return ...

# [!] {-}







# [!] {+} EXECUTION
if __name__ == "__main__":
    main()

# [!] {-}







# [!] {+} DOCSPACE
...

# [!] {-}



