from cards.card import Card
from constants.player import *
from constants.trick import *
from constants.card import *

class Trick():
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        """ Trick constructor """

        self.x_pos: float = SCREEN_WIDTH/2
        self.y_pos: float = SCREEN_HEIGHT/2

        # Player card for each trick
        self.user: Card = None
        self.east: Card = None
        self.north: Card = None
        self.west: Card = None

        self.points: int = 0
        self.hearts_broken: bool = False
        self.suit: str = None
    
    def add_card(self, player_name: str, card: Card):
        if self.is_empty() == True:
            self.suit = card.get_suit()
            print(f'Trick suit is {self.suit}')
        card.set_position(self.x_pos, self.y_pos)
        self.set_card_trick_position(player_name, card)
        if player_name == USER:
            self.user = card
        elif player_name == EAST:
            self.east = card
        elif player_name == NORTH:
            self.north = card
        elif player_name == WEST:
            self.west = card
        self.calculate_points(card)
    
    def calculate_points(self, card: Card):
        card_point = self.get_card_point(card)
        self.points += card_point
        if card_point != 0 and self.is_hearts_broken() == False:
            self.hearts_broken = True
            print('HEARTS IS BROKEN XD')
    
    def set_card_trick_position(self, player_name: str, card: Card):
        player_to_position = {
            USER: [0, -TRICK_VERTICAL_OFFSET],
            EAST: [TRICK_HORIZONTAL_OFFSET, 0],
            NORTH: [0, TRICK_VERTICAL_OFFSET],
            WEST: [-TRICK_HORIZONTAL_OFFSET, 0]           
        }
        x_offset, y_offset = player_to_position[player_name]
        card.set_position(self.x_pos+x_offset, self.y_pos+y_offset)

    def get_suit(self) -> str:
        return self.suit
    
    def set_suit(self, suit: str):
        self.suit = suit
    
    def reset(self):
        self.user = None
        self.east = None
        self.north = None
        self.west = None
        self.suit = None
        self.points = 0
    
    def is_empty(self) -> bool:
        cards = self.get_cards_list()
        for card in cards:
            if card != None:
                return False
        return True
    
    def is_hearts_broken(self) -> bool:
        return self.hearts_broken
    
    def is_full(self) -> bool:
        for p in self.get_cards_list():
            if p == None:
                return False
        return True
    
    def get_trick_winner(self, user: str, east: str, north: str, west: str) -> str:
        card_to_players = {
            self.user: user,
            self.east: east,
            self.north: north,
            self.west: west
        }
        highest_card = self.get_highest_card()
        trick_winner = card_to_players[highest_card]
        # trick_winner.add_points(self.points)
        return trick_winner
    
    def get_highest_card(self) -> Card | None:
        cards = list(filter(lambda x: x.get_suit() == self.suit, self.get_cards_list()))
        max_value = 0
        max_card = None
        for card in cards:
            card_numeric_value = card.get_numeric_value()
            if card_numeric_value > max_value:
                max_value = card_numeric_value
                max_card = card
        return max_card

    def get_card_point(self, card: Card) -> int:
        if card.get_suit() == HEARTS:
            return 1
        elif card.get_suit() == SPADES and card.get_value() == 'Q':
            return 13
        return 0 
    
    def get_points(self) -> int:
        return self.points
    
    def get_cards_list(self) -> list:
        return [self.user, self.east, self.north, self.west]

    def draw(self):
        players = self.get_cards_list()
        for p in players:
            if p != None:
                p.draw()


        