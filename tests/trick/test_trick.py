import unittest
from unittest.mock import Mock, MagicMock, patch
from players.player import Player
from trick.trick import Trick


class TrickTest(unittest.TestCase):
    def setUp(self):
        self.player_east = Player(name="EAST")
        self.player_two = Player(name="WEST")
        self.player_three = Player(name='Penguin')

        self.trick = Trick(100, 100)

        self.mock_two_clubs = MagicMock()
        self.mock_two_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_two_clubs.get_value = Mock(return_value='2')
        self.mock_two_clubs.get_numeric_value = Mock(return_value=2)

        self.mock_king_hearts = MagicMock()
        self.mock_king_hearts.get_suit = Mock(return_value='Hearts')
        self.mock_king_hearts.get_value = Mock(return_value='K')
        self.mock_king_hearts.get_numeric_value = Mock(return_value=13)

        self.mock_queen_spades = MagicMock()
        self.mock_queen_spades.get_suit = Mock(return_value='Spades')
        self.mock_queen_spades.get_value = Mock(return_value='Q')
        self.mock_queen_spades.get_numeric_value = Mock(return_value=12)
        
        self.mock_five_clubs = MagicMock()
        self.mock_five_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_five_clubs.get_numeric_value = Mock(return_value=5)

    @patch('trick.trick.Trick.get_cards_list')
    def test_is_empty(self, mock_get_cards_list):
        mock_get_cards_list.return_value = [None, None, None, None]
        self.assertTrue(self.trick.is_empty())
        mock_get_cards_list.return_value = [None, 'zero O Clock', None]
        self.assertFalse(self.trick.is_empty())

    @patch('trick.trick.Trick.get_cards_list')
    def test_is_full(self, mock_get_cards_list):
        mock_get_cards_list.return_value = [None, None, None, None]
        self.assertFalse(self.trick.is_full())
        mock_get_cards_list.return_value = ['Crystal Snow', 'zero O Clock', 'Film out']
        self.assertTrue(self.trick.is_full())

    def test_get_card_point(self):
        self.assertEqual(self.trick.get_card_point(self.mock_king_hearts), 1)
        self.assertEqual(self.trick.get_card_point(self.mock_two_clubs), 0)
        self.assertEqual(self.trick.get_card_point(self.mock_queen_spades), 13)
        
    @patch('trick.trick.Trick.get_card_point')
    def test_calculate_points(self, mock_get_card_point):
        mock_get_card_point.return_value = 0
        self.trick.calculate_points(self.mock_two_clubs)
        self.assertFalse(self.trick.is_hearts_broken())
        self.assertEqual(self.trick.get_points(), 0)

        mock_get_card_point.return_value = 1
        self.trick.calculate_points(self.mock_king_hearts)
        self.assertTrue(self.trick.is_hearts_broken())
        self.assertEqual(self.trick.get_points(), 1)

    @patch('trick.trick.Trick.set_card_trick_position')
    @patch('trick.trick.Trick.calculate_points')
    def test_add_card(self, mock_calculate_points, mock_set_card_trick_position):
        self.mock_two_clubs.set_position = Mock()
        for card in [self.trick.east, self.trick.west, self.trick.north, self.trick.user]:
            self.assertIsNone(card)
        self.trick.add_card('EAST', self.mock_two_clubs)
        self.mock_two_clubs.set_position.assert_called_once()
        mock_set_card_trick_position.assert_called_once()
        mock_calculate_points.assert_called_once_with(self.mock_two_clubs)
        self.assertEqual(self.trick.east, self.mock_two_clubs)
        for card in [self.trick.west, self.trick.north, self.trick.user]:
            self.assertIsNone(card)

        self.mock_two_clubs.set_position.reset_mock()
        mock_set_card_trick_position.reset_mock()
        mock_calculate_points.reset_mock()
            
        self.trick.add_card('WEST', self.mock_two_clubs)
        self.mock_two_clubs.set_position.assert_called()
        mock_set_card_trick_position.assert_called()
        mock_calculate_points.assert_called_once_with(self.mock_two_clubs)
        self.assertEqual(self.trick.west, self.mock_two_clubs)

        self.trick.add_card('NORTH', self.mock_queen_spades)
        self.assertEqual(self.trick.north, self.mock_queen_spades)
            
        self.trick.add_card('USER', self.mock_king_hearts)
        self.assertEqual(self.trick.user, self.mock_king_hearts)
    
    @patch('trick.trick.Trick.get_cards_list')
    def test_get_highest_card(self, mock_get_cards_list):
        self.mock_five_clubs = MagicMock()
        self.mock_five_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_five_clubs.get_numeric_value = Mock(return_value=5)
        
        mock_ace_clubs = MagicMock()
        mock_ace_clubs.get_suit = Mock(return_value='Clubs')
        mock_ace_clubs.get_numeric_value = Mock(return_value=14)
        
        self.trick.suit = 'Clubs'
        
        mock_get_cards_list.return_value = [self.mock_two_clubs]
        self.assertEqual(self.mock_two_clubs, self.trick.get_highest_card())
        
        mock_get_cards_list.return_value = [self.mock_two_clubs, self.mock_five_clubs, mock_ace_clubs]
        self.assertEqual(mock_ace_clubs, self.trick.get_highest_card())
        
        mock_get_cards_list.return_value = [self.mock_two_clubs, self.mock_five_clubs, self.mock_king_hearts]
        self.assertEqual(self.mock_five_clubs, self.trick.get_highest_card())
        
        self.trick.suit = 'Hearts'
        
        mock_get_cards_list.return_value = [self.mock_queen_spades, self.mock_king_hearts]
        self.assertEqual(self.mock_king_hearts, self.trick.get_highest_card())
        
        mock_get_cards_list.return_value = [self.mock_queen_spades]
        self.assertIsNone(self.trick.get_highest_card())
        
    @patch('trick.trick.Trick.get_highest_card')
    def test_get_trick_winner(self, mock_get_highest_card):
        self.trick.user = self.mock_two_clubs
        self.trick.east = self.mock_king_hearts
        self.trick.west = self.mock_queen_spades
        self.trick.north = self.mock_five_clubs

        mock_get_highest_card.return_value = self.mock_five_clubs
        self.assertEqual('N', self.trick.get_trick_winner('U', 'E', 'N', 'W'))

        mock_get_highest_card.return_value = self.mock_king_hearts
        self.assertEqual('E', self.trick.get_trick_winner('U', 'E', 'N', 'W'))

        mock_get_highest_card.return_value = self.mock_queen_spades
        self.assertEqual('W', self.trick.get_trick_winner('U', 'E', 'N', 'W'))
