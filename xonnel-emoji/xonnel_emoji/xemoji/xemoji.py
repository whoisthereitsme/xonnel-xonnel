import unicodedata
import regex
from .allemojis import *
from .allemojis.mapping import EmojisMapping


class XEmoji:
    RE_GRAPHEME = regex.compile(r"\X")
    RE_HAS_EMOJI = regex.compile(
        r"("
        r"\p{Extended_Pictographic}"
        r"|[\U0001F1E6-\U0001F1FF]"
        r"|[#*0-9]\uFE0F?\u20E3"
        r")"
    )
    RE_NON_NAME = regex.compile(r"[^a-z0-9_]+")
    RE_MULTI_UNDERSCORE = regex.compile(r"_+")

    DROP_NAME_PARTS = {
        "variation_selector_16",
        "variation_selector_15",
        "zero_width_joiner",
    }

    MAPPING = EmojisMapping.MAPPING

    

    def __init__(self):
        self.emojis = {}
        self.reverse = {}
        self.init()

    def init(self):
        for emoji in self.splitemojis(EmojisAll.ALL):
            name = self.getname(emoji)
            if not name:
                continue

            base = name
            i = 2
            while name in self.emojis:
                name = f"{base}_{i}"
                i += 1

            self.emojis[name] = emoji
            self.reverse[emoji] = name

    def splitemojis(self, txt: str = None):
        if not txt:
            return []

        out = []
        for part in self.RE_GRAPHEME.findall(txt):
            if part and not part.isspace() and self.isemoji(part):
                out.append(part)
        return out

    def isemoji(self, txt: str = None):
        if not txt or txt.isspace():
            return False
        return bool(self.RE_HAS_EMOJI.search(txt))

    def normalize(self, txt: str = None):
        if not txt:
            return None

        txt = str(txt).lower().replace("-", "_").replace(" ", "_")
        txt = self.RE_NON_NAME.sub("_", txt)
        txt = self.RE_MULTI_UNDERSCORE.sub("_", txt)
        txt = txt.strip("_")
        return txt or None

    def getname(self, emoji: str = None):
        if not emoji:
            return None

        parts = []
        for ch in emoji:
            try:
                name = unicodedata.name(ch).lower().replace("-", "_").replace(" ", "_")
            except ValueError:
                continue

            if name in self.DROP_NAME_PARTS:
                continue

            parts.append(name)

        if not parts:
            return "emoji_" + "_".join(f"u{ord(ch):x}" for ch in emoji)

        return self.normalize("_".join(parts))

    def score(self, query: str, candidate: str):
        if not query or not candidate:
            return float("-inf")

        qparts = query.split("_")
        cparts = candidate.split("_")

        score = 0

        if query == candidate:
            score += 1_000_000

        if query in cparts:
            score += 500_000

        if candidate.startswith(query + "_"):
            score += 200_000

        if candidate.endswith("_" + query):
            score += 150_000

        for q in qparts:
            if q in cparts:
                score += 100_000

        samepos = sum(1 for a, b in zip(query, candidate) if a == b)
        score += samepos * 100

        score += len(set(qparts) & set(cparts)) * 10_000
        score -= abs(len(query) - len(candidate)) * 10

        return score

    def find(self, name: str = None):
        if not name:
            return None

        name = str(name)

        if self.isemoji(name):
            return self.getname(name)

        query = self.normalize(name)
        if not query:
            return None

        if query in self.emojis:
            return self.emojis[query]

        best_name = None
        best_score = None

        for candidate in self.emojis:
            score = self.score(query, candidate)
            if best_score is None or score > best_score:
                best_score = score
                best_name = candidate

        if best_name is None:
            return None

        return self.emojis[best_name]






