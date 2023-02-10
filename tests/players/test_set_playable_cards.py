import unittest
from unittest.mock import call, patch, Mock, MagicMock
from players.player import Player


class SetPlayableCardsTest(unittest.TestCase):
    def setUp(self):
        self.computer_north = Player(name='North')
        self.user = Player(name='User')

        self.trick_no_suit = MagicMock()
        self.trick_no_suit.get_suit = Mock(return_value=None)
        self.trick_no_suit.is_hearts_broken.return_value = False
        self.trick_hearts = MagicMock()
        self.trick_hearts.get_suit.return_value = 'Hearts'

        self.mock_two_clubs = MagicMock()
        self.mock_two_clubs.get_suit = Mock(return_value='Clubs')
        self.mock_two_clubs.get_value = Mock(return_value='2')

        self.mock_king_hearts = MagicMock()
        self.mock_king_hearts.get_suit = Mock(return_value='Hearts')
        self.mock_king_hearts.get_value = Mock(return_value='K')

        self.mock_queen_spades = MagicMock()
        self.mock_queen_spades.get_suit = Mock(return_value='Spades')
        self.mock_queen_spades.get_value = Mock(return_value='Q')

    @patch('players.player.Player.get_two_of_clubs')
    @patch('players.player.Player.get_playable_cards')
    def test_first_round(self, mock_get_playable_cards, mock_get_two_of_clubs):
        mock_get_two_of_clubs.return_value = self.mock_two_clubs
        # Is first round and has two of clubs
        return_card = self.computer_north.set_playable_cards(self.trick_no_suit, first_round=True)
        mock_get_playable_cards.assert_not_called()

        # Is first round and does not have two of clubs
        mock_get_playable_cards.return_value = [self.mock_queen_spades]
        mock_get_two_of_clubs.return_value = None
        self.computer_north.set_playable_cards(self.trick_no_suit, first_round=True)
        mock_get_playable_cards.assert_called_once_with(False)

    @patch('players.player.Player.get_playable_cards')
    @patch('players.player.Player.get_cards')
    def test_not_first_round_player_starts(self, mock_get_cards, mock_get_playable_cards):
        # Is not first round and computer is starting
        self.computer_north.set_playable_cards(self.trick_no_suit, first_round=False)
        mock_get_cards.assert_called()

    @patch('players.player.Player.get_playable_cards')
    @patch('players.player.Player.get_cards')
    def test_not_first_round_player_not_starting_has_suit(self, mock_get_cards, mock_get_playable_cards):
        # Is not first round and computer is not starting and has suit
        mock_get_cards.return_value = [self.mock_two_clubs, self.mock_king_hearts]
        self.computer_north.set_playable_cards(self.trick_hearts, first_round=False)
        mock_get_cards.assert_called_once()

    @patch('players.player.Player.get_playable_cards')
    @patch('players.player.Player.get_cards')
    def test_not_first_round_player_not_starting_no_suit(self, mock_get_cards, mock_get_playable_cards):
        # Is not first round and computer is not starting and does not have suit
        mock_get_cards.return_value = [self.mock_two_clubs]
        self.computer_north.set_playable_cards(self.trick_hearts, first_round=False)
        mock_get_cards.assert_has_calls([call(), call()])  # Should call method twice


if __name__ == '__main__':
    unittest.main()
