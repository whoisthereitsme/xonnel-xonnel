from pathlib import Path
import subprocess
import sys


class Install:
    BASE = Path(r"C:\Code\Python\Packages")

    def __init__(self, filter="xonnel"):
        packages = []
        for d in self.BASE.iterdir():
            if d.is_dir() and d.name.startswith(filter):
                packages.append(d)

        n = len(packages)
        print(f"Found {n} packages to install.")

        for i, d in enumerate(packages, 1):
            print(f"[INSTALLING] [{i}/{n}] {d}")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "."],
                    cwd=d,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            except Exception as e:
                print(f"[INSTALLING] [FAILED] {e}")


if __name__ == "__main__":
    Install("xonnel")