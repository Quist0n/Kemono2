from dataclasses import dataclass

from src.internals.types import AbstractDataclass
# from .base import Paysite
from .discord import Discord
from .dlsite import DLSite
from .fanbox import Fanbox
from .fantia import Fantia
from .gumroad import Gumroad
from .patreon import Patreon
from .subscribestar import Subscribestar

# from typing import List

@dataclass
class Paysites(AbstractDataclass):
    discord: Discord = Discord()
    dlsite: DLSite = DLSite()
    fanbox: Fanbox = Fanbox()
    fantia: Fantia = Fantia()
    gumroad: Gumroad = Gumroad()
    patreon: Patreon = Patreon()
    subscribestar: Subscribestar = Subscribestar()
