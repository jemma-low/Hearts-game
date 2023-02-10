from arcade import SpriteList
from constants.player import *
from constants.card import *
from constants.screen import X_SPACING, Y_SPACING
from position import Position
from cards.card import Card
from trick.trick import Trick


class Player():
    """ Player sprite """

    def __init__(self, name: str):
        """ Player constructor """

        # Attributes for suit and value
        self.name: str = name
        self.cards: SpriteList = SpriteList()
        self.start_position: Position = None
        self.next_position: Position = None
        self.points: int = 0
        self.next_player: Player = None
        self.card_shift: tuple = None
        self.playable_cards: list | SpriteList = []

        if name in [EAST, WEST]: 
            self.card_shift = lambda x, y: (x, y+Y_SPACING)
        else:
            self.card_shift = lambda x, y: (x-X_SPACING, y)
    
    def set_starting_position(self, position: Position):
        self.start_position = position
        self.next_position = position
    
    def get_next_position(self) -> Position:
        return self.next_position

    def set_next_position(self, position: Position):
        self.next_position = position
    
    def get_name(self) -> str:
        return self.name
    
    def get_cards(self) -> SpriteList:
        return self.cards
    
    def get_number_of_cards(self) -> int:
        return len(self.cards)

    def add_card(self, card: Card):
        self.cards.append(card)  

    def remove_card(self, card: Card):
        index = self.cards.index(card)
        self.cards.remove(card)
        self.shift_cards(index)
    
    def get_next_player(self):
        print('next player', self.next_player.get_name())
        return self.next_player
    
    def set_next_player(self, player):
        self.next_player = player
    
    def draw_cards(self):
        self.cards.draw()
    
    def get_points(self) -> int:
        return self.points
    
    def set_points(self, value: int):
        self.points = value
    
    def add_points(self, value: int):
        current_points = self.get_points()
        self.set_points(current_points+value)
    
    def reset_points(self):
        self.points = 0

    def set_playable_cards(self, trick: Trick, first_round: bool):
        # First round
        if first_round:
            # Check for two of clubs
            card = self.get_two_of_clubs()
            if card != None:
                self.playable_cards = [card]
                return

        suit = trick.get_suit()
        # Player does not have suit
        if suit == None:
            if first_round == True:
                self.playable_cards = self.get_playable_cards(trick.is_hearts_broken())
            else:
                self.playable_cards = self.get_cards()
            return

        # Player does not start trick
        self.playable_cards = list(filter(lambda x: x.get_suit() == suit, self.get_cards()))
        if len(self.playable_cards) == 0:
            self.playable_cards = self.get_cards()

    def get_playable_cards(self, is_hearts_broken: bool) -> (SpriteList | list):
        if is_hearts_broken == False:
            cards = list(filter(lambda x: x.get_suit() != HEARTS, self.get_cards()))
            if len(cards) == 0:
                return self.get_cards()
        else:
            cards = self.get_cards()
        return cards

    def play_card(self):
        pass

    def shift_cards(self, index: int):
        card_shift_list = self.cards
        for i in range(index, len(card_shift_list)):
            old_x = self.cards[i].center_x
            old_y = self.cards[i].center_y
            new_position = self.card_shift(old_x, old_y)
            card_shift_list[i].set_position(new_position[0], new_position[1])
    
    def get_two_of_clubs(self) -> (Card | None):
        for card in self.get_cards():
            if card.get_suit() == CLUBS and card.get_value() == '2':
                return card
        return None
