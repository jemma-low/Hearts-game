import unittest
from unittest.mock import Mock, MagicMock
from players.player import Player
from cards.card import Card


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player_one = Player(name="EAST")
        self.player_two = Player(name="WEST")
        self.player_three = Player(name='Penguin')

        self.mock_two_clubs = MagicMock()
        self.mock_two_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_two_clubs.get_value = Mock(return_value='2')

        self.mock_king_hearts = MagicMock()
        self.mock_king_hearts.get_suit = Mock(return_value='Hearts')
        self.mock_king_hearts.get_value = Mock(return_value='K')

        self.mock_queen_spades = MagicMock()
        self.mock_queen_spades.get_suit = Mock(return_value='Spades')
        self.mock_queen_spades.get_value = Mock(return_value='Q')        
        
        self.cards_with_two_clubs = [
            self.mock_two_clubs,
            self.mock_king_hearts,
            self.mock_queen_spades
        ]
        self.cards_no_two_clubs = [
            self.mock_king_hearts,
            self.mock_queen_spades
        ]
    
    def test_get_name(self):
        self.assertEqual(self.player_one.get_name(), 'EAST')
        self.assertEqual(self.player_two.get_name(), 'WEST')
        self.assertEqual(self.player_three.get_name(), 'Penguin')
    
    def test_next_player(self):
        self.player_one.set_next_player(self.player_two)
        self.assertEqual(self.player_one.get_next_player(), self.player_two)
        self.player_two.set_next_player(self.player_one)
        self.assertEqual(self.player_two.get_next_player(), self.player_one)
        self.player_three.set_next_player(self.player_three)
        self.assertEqual(self.player_three.get_next_player(), self.player_three)

    def test_card_methods(self):
        for card in self.cards_with_two_clubs:
            self.player_one.add_card(card)
        self.assertCountEqual(self.cards_with_two_clubs, self.player_one.get_cards())
        self.assertEqual(self.player_one.get_number_of_cards(), len(self.cards_with_two_clubs))
        self.player_one.remove_card(self.mock_two_clubs)
        self.assertEqual(self.player_one.get_number_of_cards(), len(self.cards_with_two_clubs)-1)

    def test_get_two_of_clubs(self):
        for card in self.cards_with_two_clubs:
            self.player_one.add_card(card)
        for card in self.cards_no_two_clubs:
            self.player_two.add_card(card)
        self.assertEqual(self.player_one.get_two_of_clubs(), self.mock_two_clubs)
        self.assertIsNone(self.player_two.get_two_of_clubs())

    def test_get_playable_cards(self):
        for card in self.cards_with_two_clubs:
            self.player_one.add_card(card)

        cards_hearts_broken = [
            self.mock_two_clubs, 
            self.mock_king_hearts,
            self.mock_queen_spades
        ]
        cards_hearts_unbroken = [
            self.mock_two_clubs, 
            self.mock_queen_spades
        ]
        self.assertCountEqual(
            self.player_one.get_playable_cards(True), cards_hearts_broken
        )
        self.assertCountEqual(
            self.player_one.get_playable_cards(False), cards_hearts_unbroken
        )

    # Test getter, setter and adding point methods. Can assume points will always be positive.
    def test_points(self):
        self.assertEqual(self.player_one.get_points(), 0)
        self.player_one.add_points(value=3)
        self.assertEqual(self.player_one.get_points(), 3)
        self.player_one.reset_points()
        self.assertEqual(self.player_one.get_points(), 0)