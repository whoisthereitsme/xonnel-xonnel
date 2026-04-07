from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...








from pathlib import Path

from xonnel_file import XFile



import datetime
import time




















class XBackup:
    MODES = ["ZIP", "FILES"]
    def __init__(self, path:str|Path=None, mode:str="ZIP"):
        self.path = Path(path)
        self.mode = mode

        if mode == "FILES":
            self.backup_files(src=self.path)

        if mode == "ZIP":
            self.backup_zip(src=self.path)

    def backup_files(self, src:Path=None):
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


    def backup_zip(self, src:Path=None):
        t0 = time.time()    
        srcname = src.stem
        tgtdir = Path(r"D:\Backups")
        tgtname = srcname + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        tgt = tgtdir / srcname / tgtname
        tempzip = Path(r"C:\Code\.temp\backup.zip")
        tempdir = Path(r"C:\Code\.temp\backup")
        paths = XFile.walk(path=src, exc=["__pycache__", ".git", ".pyc"])
        for path in paths:
            if path.is_file():
                relpath = path.relative_to(src)
                temppath = tempdir / relpath
                XFile.copy(src=path, tgt=temppath)

        XFile.pack(src=tempdir, tgt=tempzip)
        size = tempzip.stat().st_size
        print(f"Zipped:\nsrc:  {src}\ntgt:  {tgt}\nsize: {round(size/(1024*1024), 2)} MB")
        XFile.move(src=tempzip, tgt=tgt)
        XFile.delete(path=tempdir)

        t1 = time.time()
        t = t1 - t0
        print(f"Backed up:\nsrc:  {src}\ntgt:  {tgt}\ntime: {t:.2f} seconds!\n\n")











if __name__ == "__main__":
    # USAGE: 2 modes: "FILES" or "ZIP"
    XBackup(path=Path(r"C:\Code"), mode="FILES")
    XBackup(path=Path(r"C:\Code"), mode="ZIP")