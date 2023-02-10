import unittest
from unittest.mock import call, patch, Mock, MagicMock
from players.user import User


class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User(name='User')

        self.mock_two_clubs = MagicMock()
        self.mock_two_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_two_clubs.get_value = Mock(return_value='2')

        self.mock_king_hearts = MagicMock()
        self.mock_king_hearts.get_suit = Mock(return_value='Hearts')
        self.mock_king_hearts.get_value = Mock(return_value='K')

        self.mock_queen_spades = MagicMock()
        self.mock_queen_spades.get_suit = Mock(return_value='Spades')
        self.mock_queen_spades.get_value = Mock(return_value='Q')

    @patch('players.player.Player.get_playable_cards')
    def test_can_play_card(self, mock_get_playable_cards):
        self.user.playable_cards = [self.mock_queen_spades, self.mock_king_hearts]
        self.assertTrue(self.user.can_play_card(self.mock_king_hearts))
        self.assertFalse(self.user.can_play_card(self.mock_two_clubs))


if __name__ == '__main__':
    unittest.main()