"""
Solitaire clone.
"""
import arcade
from constants.screen import *
from cards.card import Card
from constants.card import *
from constants.player import *
from players.user import User
from players.computer import Computer
from players.player import Player
from position import Position
from trick.trick import Trick
import random
import time


class Game(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

        self.passing: bool = False
        self.round_end: bool = False

        # Create Players
        self.create_players()

        self.first_round: bool = True
        self.current_player: Player = None

    def setup(self, is_debug: bool):
        """ Set up the game here. Call this function to restart the game. """
        print('set up game')

        # Cards in trick
        self.trick: Trick = Trick(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create every card
        self.create_cards(is_debug)

        print('==== Game start ====\n')

    def create_players(self):
        self.user = User(USER)
        self.north = Computer(NORTH)
        self.east = Computer(EAST)
        self.west = Computer(WEST)
        self.user.set_next_player(self.east)
        self.east.set_next_player(self.north)
        self.north.set_next_player(self.west)
        self.west.set_next_player(self.user)

    def create_cards(self, is_debug):
        self.user.set_starting_position(USER_POSITION)
        self.north.set_starting_position(NORTH_POSITION)
        self.east.set_starting_position(EAST_POSITION)
        self.west.set_starting_position(WEST_POSITION)

        players = [self.user, self.north, self.east, self.west]

        # Start with user cards first
        count = 0
        card_values_list = CARD_VALUES.copy()
        for card_suit in SUITS:
            for card_value in card_values_list:
                card = Card(card_suit, card_value, CARD_SCALE)
                if is_debug:
                    card.face_up()

                # Randomly select player to allocate card to
                p_index = random.randrange(len(players))
                player = players[p_index]
                position = player.get_next_position()
                x_pos = position.x_pos
                y_pos = position.y_pos
                card.set_original_position(x_pos, y_pos)
                if player.get_name() == USER or player.get_name() == NORTH:
                    player.set_next_position(Position(x_pos + X_SPACING, y_pos))
                    if player.get_name() == USER:
                        card.face_up()
                else:
                    player.set_next_position(Position(x_pos, y_pos - Y_SPACING))

                player.add_card(card)
                if card_suit == CLUBS and card.value == '2':
                    self.current_player = player

                if player.get_number_of_cards() >= 13:
                    players.pop(p_index)
                count += 1

    def next_current_player(self):
        current_player_dict = {
            USER: self.east,
            EAST: self.north,
            NORTH: self.west,
            WEST: self.user
        }
        self.current_player = current_player_dict[self.current_player.get_name()]

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the cards
        self.user.draw_cards()
        self.east.draw_cards()
        self.north.draw_cards()
        self.west.draw_cards()
        self.trick.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Can only click on a card if its user's turn
        if self.current_player.get_name() != USER or self.round_end == True:
            return

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.user.get_cards())

        # Have we clicked on a card?
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            if self.passing:
                # TODO implement passing logic
                pass
            else:
                if self.user.can_play_card(primary_card) == False:
                    return
                # Add card to trick and move to center
                self.trick.add_card(self.user.get_name(), primary_card)
                print(f'{self.user.get_name()} plays {primary_card.get_card_formatted()}')
                self.user.remove_card(primary_card)
                self.on_draw()  # User rendering doesn't always work when east starts
                self.get_next_player(self.user)

    def on_update(self, delta_time: float):
        if self.round_end == True:
            return
        if self.trick.is_full():
            self.on_draw()  # User rendering doesn't always work when east starts
            # Round end
            if len(self.current_player.get_cards()) == 0:
                self.round_end = True
                self.trick.get_trick_winner(self.user, self.east, self.north, self.west)
                self.display_scoreboard()
                return
            self.current_player = self.get_trick_winner()
            self.current_player.add_points(self.trick.get_points())
            print(f'trick winner: {self.current_player.get_name()}')
            print()
            time.sleep(3)
            self.trick.reset()
            if self.first_round == True:
                self.first_round == False
            return
        if self.current_player.get_name() == USER:
            self.current_player.set_playable_cards(self.trick, self.first_round)
            return
        self.current_player.set_playable_cards(self.trick, self.first_round)
        card = self.current_player.play_card()
        card.face_up()
        self.trick.add_card(self.current_player.get_name(), card)
        print(f'{self.current_player.get_name()} plays {card.get_card_formatted()}')
        self.current_player.remove_card(card)
        self.get_next_player(self.current_player)

    def get_trick_winner(self) -> Player:
        trick_winner_name = self.trick.get_trick_winner(
            self.user.get_name(),
            self.east.get_name(),
            self.north.get_name(),
            self.west.get_name()
        )
        trick_winner_dict = {
            USER: self.user,
            EAST: self.east,
            NORTH: self.north,
            WEST: self.west
        }
        return trick_winner_dict[trick_winner_name]

    def get_next_player(self, player) -> Player:
        self.current_player = player.get_next_player()

    def display_scoreboard(self):
        players = [self.user, self.east, self.west, self.north]
        min_points = 30
        shot_the_moon = False
        winner = None
        for p in players:
            if p.get_points() == 26:
                shot_the_moon = True
                winner = p
                break
            if p.get_points() < min_points:
                min_points = p.get_points()
                winner = p
            print(p.get_name(), p.get_points())
        print(f'Round winner: {winner.get_name()}')
        if shot_the_moon == True:
            print(f'{winner.get_name()} shot the moon!')
