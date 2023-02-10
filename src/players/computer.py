from enum import Enum
from cards.card import Card
from . player import Player
from trick.trick import Trick
from constants.screen import X_SPACING, Y_SPACING
from random import choice


class Computer(Player):
    """ User sprite """

    def __init__(self, name: str):
        """ User constructor """
        # Call the parent
        super().__init__(name)
    
    def play_card(self) -> Card:
        return choice(self.playable_cards)


