from .animals import EmojisAnimals
from .food import EmojisFood
from .people import EmojisPeople
from .symbols import EmojisSymbols
from .sports import EmojisSports
from .vehicles import EmojisVehicles
from .special import EmojisSpecial


class EmojisAll:
    ALL = (
        EmojisAnimals.EMOJIS
        + EmojisFood.EMOJIS
        + EmojisPeople.EMOJIS
        + EmojisSymbols.EMOJIS
        + EmojisSports.EMOJIS
        + EmojisVehicles.EMOJIS
        + EmojisSpecial.EMOJIS
    ).replace("\n", "").replace(" ", "")






