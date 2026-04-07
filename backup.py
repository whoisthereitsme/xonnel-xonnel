

from xonnel_backup import XBackup






def backup(src:str=None):
    XBackup(path=src, mode="ZIP")


if __name__ == "__main__":
    backup(src=r"C:\Code")