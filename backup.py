


from pathlib import Path

from xonnel_file import XFile



import datetime
import time







def backup(src:Path=None):
    t0 = time.time()
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    srcname = src.stem
    tgtdir = Path(r"D:\Backups")
    tgtname = srcname + "_" + now
    tgt = tgtdir / srcname / tgtname
    print(f"Backing up {src} to {tgt}...")
    n = 0
    t = 0
    s = 0
    d = 0
    paths = XFile.walk(path=src, exc=["__pycache__", ".git", ".pyc"])

    for path in paths:
        if path.is_file():
            t += 1
            s += path.stat().st_size

    for path in paths:
        path = Path(path)
        if path.is_file():
            d += path.stat().st_size
            n += 1
            relpath = path.relative_to(src)
            tgtpath = tgt / relpath
            XFile.copy(src=path, tgt=tgtpath)
            print(f"Backed up file:\nindex: {n}/{t}\nsrc:   {path}\ntgt:   {tgtpath}\ntodo:  {round((s-d)/(1024*1024), 2)} MB\n")


    t1 = time.time()
    t = t1 - t0
    print(f"Backed up:\nsrc:  {src}\ntgt:  {tgt}\ntime: {t:.2f} seconds!\n\n")


if __name__ == "__main__":
    backup(src=Path(r"C:\Code"))