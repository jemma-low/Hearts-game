from arcade import SpriteList
from . player import Player
from trick.trick import Trick
from cards.card import Card

class User(Player):
    """ User sprite """

    def __init__(self, name: str):
        """ User constructor """
        self.can_play: bool = True

        # Call the parent
        super().__init__(name)
    
    def can_play_card(self, card: Card) -> bool:
        if card in self.playable_cards:
            return True
        return False
