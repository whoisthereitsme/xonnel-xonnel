


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
    # XFile.copy(src=src, tgt=tgt)
    t1 = time.time()
    t = t1 - t0
    print(f"Backed up {src} to {tgt} in {t:.2f} seconds!")



if __name__ == "__main__":
    backup(src=Path(r"C:\Code"))