


from pathlib import Path

from xonnel_file import XFile



def main(filter=None):
    XFile.copy(src=Path(r"C:\Code\Python\Packages\backup"), dst=Path(r"C:\Code\Python\Packages\backup2"), filter=filter, overwrite=True, verbose=True)