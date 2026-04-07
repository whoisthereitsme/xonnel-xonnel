


from pathlib import Path

from xonnel_file import XFile



import datetime
import time





def main():
    t0 = time.time()
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    src = Path(r"C:\Code")
    tgt = Path(r"D:\Backups\Code") / f"Code_{time_str}"
    print(f"Backing up {src} to {tgt}...")
    XFile.copy(src=src, tgt=tgt)
    t1 = time.time()
    t = t1 - t0
    print(f"Backed up {src} to {tgt} in {t:.2f} seconds!")



if __name__ == "__main__":
    main()