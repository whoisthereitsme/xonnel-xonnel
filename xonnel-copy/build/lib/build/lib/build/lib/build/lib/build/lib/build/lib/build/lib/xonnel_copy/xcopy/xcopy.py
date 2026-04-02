from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






from pathlib import Path
import shutil







class XCopy:
    def __init__(self, src:str|Path=None, tgt:str|Path=None):
        try:
            if src is None or tgt is None:
                print("[ERROR] [XCopy] [src and tgt cannot be None]")
                return False

            src = Path(src)
            tgt = Path(tgt)

            if not src.exists():
                print(f"[ERROR] [XCopy] [Source does not exist: {src}]")
                return False

            tgt.parent.mkdir(parents=True, exist_ok=True)

            if src.is_file():
                if tgt.exists() and tgt.is_dir():
                    tgt = tgt / src.name

                shutil.copy2(src, tgt)

            elif src.is_dir():
                if tgt.exists():
                    shutil.rmtree(tgt)
                shutil.copytree(src, tgt)

            else:
                print(f"[ERROR] [XCopy] [Unsupported src type: {src}]")
                return False

            return True

        except Exception as e:
            print(f"[ERROR] [XCopy] [Error copying {src} -> {tgt}: {e}]")
            return False






