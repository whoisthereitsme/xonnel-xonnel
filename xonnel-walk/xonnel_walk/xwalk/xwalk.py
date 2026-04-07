from pathlib import Path



class XWalk:
    DEFAULT_EXC = [
        "__pycache__",
        ".git",
   ]
    def __init__(self, path:str|Path=None, inc:list[str]=None, exc:list[str]=None, deep:int=None):
        self.path = Path(path).resolve() if path is not None else Path.cwd()
        self.inc = inc
        self.exc = exc
        self.deep = deep

    def __iter__(self):
        yield from self.walk(path=self.path, deep=self.deep)

    def walk(self, path:Path=None, deep:int=None):
        if deep is not None and deep <= 0:
            return

        for item in path.iterdir():
            if self.inc and not any(item.match(p) for p in self.inc):
                continue

            if self.exc and any(item.match(p) for p in self.exc):
                continue

            yield item

            if item.is_dir():
                newdeep = deep - 1 if deep is not None else None
                yield from self.walk(path=item, deep=newdeep)







