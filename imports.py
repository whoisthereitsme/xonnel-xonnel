from pathlib import Path


class Imports:
    def __init__(self, root:str|Path=None):
        self.root = Path(root) if root else Path.cwd()

        self.scan()

    def scan(self):
        self.lines = []
        toexclude = []
        for path in self.root.rglob("*.py"): 
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if "import" in line:
                            stripped = line.strip()
                            if stripped.startswith("from ."):
                                toexclude.append(stripped)
                                toexclude.append(stripped.replace("from .", "from "))
                            if "xonnel" in stripped:
                                toexclude.append(stripped)
                      
            except Exception:
                continue

        for path in self.root.rglob("*.py"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if "import" in line:
                            stripped = line.strip()
                            if stripped not in toexclude and stripped not in self.lines:
                                self.lines.append(stripped)
            except Exception:
                continue

        for line in self.lines:
            print(line)


if __name__ == "__main__":
    Imports(root=r"C:\Code\Python\Packages")



