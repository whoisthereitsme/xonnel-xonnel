from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ...






import os
import sys
import re
import random





from pathlib import Path
from xonnel_pad import XPad







class XGame:
    STEAM_PATH = Path(r"C:\Program Files (x86)\Steam")

    STEAM_BY_TITLE = {}
    STEAM_BY_INDEX = {}
    TITLE_BY_STEAM = {}
    TITLE_BY_INDEX = {}
    INDEX_BY_TITLE = {}
    INDEX_BY_STEAM = {}

    def __init__(self, game: str = ""):
        self.game: str = str(game).strip()
        self.index: str | None = None
        self.steam: str | None = None
        self.title: str | None = None

        self.init()
        self.find()
        self.play()

    def init(self):
        games = self.games()

        self.real = []
        self.found = [["INDEX", "STEAM-ID", "TITLE"]]

        for index, (title, steam) in enumerate(games.items(), start=1):
            self.real.append([str(index), steam, title])

        self.random_index = str(len(self.real) + 1)
        self.exit_index = "0"

        self.found += self.real
        self.found += [[self.random_index, "None", "PLAY A RANDOM GAME"]]
        self.found += [[self.exit_index, "None", "EXIT MENU"]]

        XGame.STEAM_BY_TITLE = {title: steam for index, steam, title in self.real}
        XGame.STEAM_BY_INDEX = {index: steam for index, steam, title in self.real}
        XGame.TITLE_BY_STEAM = {steam: title for index, steam, title in self.real}
        XGame.TITLE_BY_INDEX = {index: title for index, steam, title in self.real}
        XGame.INDEX_BY_TITLE = {title: index for index, steam, title in self.real}
        XGame.INDEX_BY_STEAM = {steam: index for index, steam, title in self.real}

    def find(self):
        while True:
            self.game = str(self.game).strip()

            if self.game == self.exit_index or self.game == "EXIT MENU":
                self.index = self.exit_index
                self.steam = None
                self.title = "EXIT MENU"
                return

            if self.game == self.random_index or self.game == "PLAY A RANDOM GAME":
                self.game = self.random()
                continue

            if self.game in XGame.STEAM_BY_TITLE:
                self.steam = XGame.STEAM_BY_TITLE[self.game]
                self.title = self.game
                self.index = XGame.INDEX_BY_TITLE[self.game]
                print(f"Found {self.title} with Steam ID: {self.steam}")
                return

            if self.game in XGame.STEAM_BY_INDEX:
                self.steam = XGame.STEAM_BY_INDEX[self.game]
                self.title = XGame.TITLE_BY_INDEX[self.game]
                self.index = self.game
                print(f"Found {self.title} with Steam ID: {self.steam}")
                return

            if self.game in XGame.TITLE_BY_STEAM:
                self.steam = self.game
                self.title = XGame.TITLE_BY_STEAM[self.game]
                self.index = XGame.INDEX_BY_STEAM[self.game]
                print(f"Found {self.title} with Steam ID: {self.steam}")
                return

            print("\nAvailable games:\n")
            print(XPad(text=self.found))
            print("\n")
            self.game = input("Enter a INDEX, TITLE or STEAM-ID to select a game: ... ").strip()
            print("\n")

    def play(self):
        if self.index == self.exit_index:
            print("Exiting menu.")
            return

        if self.steam is None:
            print("No game selected.")
            return

        url = f"steam://run/{self.steam}"

        try:
            os.startfile(url)
            print(f"Launching: {self.title}")
        except Exception as e:
            print(f"Failed to launch {self.title}: {e}")

    def random(self):
        return random.choice(list(XGame.STEAM_BY_TITLE.keys()))

    @classmethod
    def libraries(cls, path: Path = None):
        if path is None:
            return []

        vdf = path / "steamapps" / "libraryfolders.vdf"
        paths = []

        if not vdf.exists():
            return [path]

        text = vdf.read_text(encoding="utf-8", errors="ignore")
        matches = re.findall(r'"path"\s*"([^"]+)"', text)

        for m in matches:
            paths.append(Path(m.replace("\\\\", "\\")))

        paths.append(path)

        seen = set()
        out = []

        for p in paths:
            s = str(p).lower()
            if s not in seen:
                seen.add(s)
                out.append(p)

        return out

    @classmethod
    def manifest(cls, path: Path = None):
        if path is None:
            return None, None

        text = path.read_text(encoding="utf-8", errors="ignore")

        id_match = re.search(r'"appid"\s*"(\d+)"', text)
        name_match = re.search(r'"name"\s*"([^"]+)"', text)

        appid = id_match.group(1) if id_match else None
        name = name_match.group(1) if name_match else None

        return appid, name

    @classmethod
    def games(cls):
        libraries = cls.libraries(path=cls.STEAM_PATH)
        games = {}

        for lib in libraries:
            steamapps: Path = lib / "steamapps"
            if not steamapps.exists():
                continue

            for file in steamapps.glob("appmanifest_*.acf"):
                appid, name = cls.manifest(path=file)

                if appid and name:
                    games[name] = appid

        return games


def getgame():
    return sys.argv[1] if len(sys.argv) > 1 else ""


if __name__ == "__main__":
    XGame(game=getgame())