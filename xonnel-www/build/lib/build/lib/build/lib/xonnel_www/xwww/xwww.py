# [!] {+} IMPORTS
from typing import TYPE_CHECKING
# [|] {+} IMPORTS TYPING
if TYPE_CHECKING:
    ...
# [|] {-}


# [|] {+} IMPORTS 3RD PARTY
from pathlib import Path
from bs4 import BeautifulSoup
from pydantic_core import Url
from urllib import request
# [|] {-}
# [!] {-}




# [!] {+} CLASSES
class XWww:
    RETRIES = 5
    AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    REFERER = "https://www.farming-simulator.com/"

    @classmethod
    def _getheaders(cls, agent: str = None, referer: str = None):
        return {
            "User-Agent": agent if agent is not None else cls.AGENT,
            "Referer": referer if referer is not None else cls.REFERER,
        }

    @classmethod
    def html(cls, url: str | Url = None, save: str | Path = None, retries: int = None, agent: str = None, referer: str = None):
        if url is None:
            print("[ERROR] [XWww.html()] [url cannot be None]")
            return None

        retries = retries if retries is not None else cls.RETRIES
        headers = cls._getheaders(agent=agent, referer=referer)
        url = Url(str(url))

        attempt = 0

        while attempt < retries:
            attempt += 1
            try:
                req = request.Request(str(url), headers=headers)
                with request.urlopen(req) as r:
                    html = BeautifulSoup(
                        r.read().decode("utf-8", errors="ignore"),
                        "html.parser"
                    )

                if save is not None:
                    path = Path(save)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(str(html))

                return html

            except Exception:
                pass

        print(f"[ERROR] [XWww.html()] [failed after {retries} retries]")
        return None

    @classmethod
    def download(cls, url: str | Url = None, save: str | Path = None, retries: int = None, agent: str = None, referer: str = None):
        if url is None:
            print("[ERROR] [XWww.download()] [url cannot be None]")
            return None

        retries = retries if retries is not None else cls.RETRIES
        headers = cls._getheaders(agent=agent, referer=referer)
        url = Url(str(url))

        attempt = 0

        while attempt < retries:
            attempt += 1
            try:
                req = request.Request(str(url), headers=headers)
                with request.urlopen(req) as r:
                    data = r.read()

                if save is not None:
                    path = Path(save)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, "wb") as f:
                        f.write(data)

                return data

            except Exception:
                pass

        print(f"[ERROR] [XWww.download()] [failed after {retries} retries]")
        return None

# [!] {-}