# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XPng:
    @classmethod
    def load(cls, path: str | Path = None):
        try:
            if path is None:
                print("[ERROR] [XPng.load()] [Path cannot be None]")
                return None

            path = Path(path)
            img = Image.open(path)
            return img.copy()

        except FileNotFoundError as e:
            print(f"[ERROR] [XPng.load()] [Error loading PNG from {path}: {e}]")
            return None

        except Exception as e:
            print(f"[ERROR] [XPng.load()] [Unexpected error loading PNG from {path}: {e}]")
            return None




    @classmethod
    def save(cls, path: str | Path = None, data: Image.Image = None):
        try:
            if path is None:
                print("[ERROR] [XPng.save()] [Path cannot be None]")
                return False

            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            if data is None:
                print("[ERROR] [XPng.save()] [Data cannot be None]")
                return False

            if not isinstance(data, Image.Image):
                print(f"[ERROR] [XPng.save()] [Data must be PIL.Image.Image, got {type(data).__name__}]")
                return False

            data.save(path, format="PNG")
            return True

        except Exception as e:
            print(f"[ERROR] [XPng.save()] [Error saving PNG to {path}: {e}]")
            return False




    @classmethod
    def new(cls, size: tuple = (128, 128), color: tuple = (0, 0, 0, 255), save: str | Path = None, text: str = None):
        try:
            if size is None:
                size = (128, 128)

            if not isinstance(size, (tuple, list)) or len(size) != 2:
                print("[ERROR] [XPng.new()] [size must be a tuple/list like (width, height)]")
                return None

            width = int(size[0])
            height = int(size[1])

            if width <= 0 or height <= 0:
                print("[ERROR] [XPng.new()] [size values must be > 0]")
                return None

            if color is None:
                color = (0, 0, 0, 255)

            if not isinstance(color, (tuple, list)):
                print("[ERROR] [XPng.new()] [color must be a tuple/list]")
                return None

            if len(color) == 3:
                color = (int(color[0]), int(color[1]), int(color[2]), 255)

            elif len(color) == 4:
                color = (int(color[0]), int(color[1]), int(color[2]), int(color[3]))

            else:
                print("[ERROR] [XPng.new()] [color must have 3 or 4 values]")
                return None

            img = Image.new("RGBA", (width, height), color)

            if text is not None and str(text) != "":
                text = str(text)
                draw = ImageDraw.Draw(img)

                brightness = (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000
                fg = (255, 255, 255, 255) if brightness < 128 else (0, 0, 0, 255)

                max_font_size = min(width, height)
                best_font = None
                best_bbox = None

                for font_size in range(max_font_size, 1, -1):
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except Exception:
                        try:
                            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
                        except Exception:
                            font = ImageFont.load_default()

                    bbox = draw.textbbox((0, 0), text, font=font)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]

                    if tw <= width * 0.9 and th <= height * 0.9:
                        best_font = font
                        best_bbox = bbox
                        break

                    if font == ImageFont.load_default():
                        best_font = font
                        best_bbox = bbox
                        break

                if best_font is None:
                    best_font = ImageFont.load_default()
                    best_bbox = draw.textbbox((0, 0), text, font=best_font)

                tw = best_bbox[2] - best_bbox[0]
                th = best_bbox[3] - best_bbox[1]
                x = (width - tw) / 2 - best_bbox[0]
                y = (height - th) / 2 - best_bbox[1]

                draw.text((x, y), text, font=best_font, fill=fg)

            if save is not None:
                ok = cls.save(path=save, data=img)
                if not ok:
                    return None

            return img

        except Exception as e:
            print(f"[ERROR] [XPng.new()] [Unexpected error creating PNG: {e}]")
            return None

# [!] {-}