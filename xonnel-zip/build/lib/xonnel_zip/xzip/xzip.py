# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
import zipfile
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XZip:
    @classmethod
    def zip(cls, src: str | Path = None, tgt: str | Path = None):
        try:
            if src is None or tgt is None:
                print("[ERROR] [XZip.zip()] [src and tgt cannot be None]")
                return False

            src = Path(src)
            tgt = Path(tgt)

            if not src.exists():
                print(f"[ERROR] [XZip.zip()] [Source does not exist: {src}]")
                return False

            tgt.parent.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(tgt, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                if src.is_file():
                    zf.write(src, arcname=src.name)

                elif src.is_dir():
                    for p in src.rglob("*"):
                        if p.is_file():
                            zf.write(p, arcname=p.relative_to(src))

                else:
                    print(f"[ERROR] [XZip.zip()] [Unsupported src type: {src}]")
                    return False

            return True

        except Exception as e:
            print(f"[ERROR] [XZip.zip()] [Error zipping {src} -> {tgt}: {e}]")
            return False

    @classmethod
    def unzip(cls, src: str | Path = None, tgt: str | Path = None):
        try:
            if src is None or tgt is None:
                print("[ERROR] [XZip.unzip()] [src and tgt cannot be None]")
                return False

            src = Path(src)
            tgt = Path(tgt)

            if not src.exists():
                print(f"[ERROR] [XZip.unzip()] [Source does not exist: {src}]")
                return False

            tgt.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(src, "r") as zf:
                zf.extractall(tgt)

            return True

        except Exception as e:
            print(f"[ERROR] [XZip.unzip()] [Error unzipping {src} -> {tgt}: {e}]")
            return False

# [!] {-}