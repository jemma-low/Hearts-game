import unittest
from src.cards.card import Card
from src.constants.card import *


class CardTest(unittest.TestCase):
    def setUp(self):
        self.card_face = Card(suit='Clubs', value='K')
        self.card_number = Card(suit='Hearts', value='5')

    def test_get_suit(self):
        self.assertEqual(self.card_face.get_suit(), 'Clubs')
        self.assertEqual(self.card_number.get_suit(), 'Hearts')
    
    def test_get_value(self):
        self.assertEqual(self.card_face.get_value(), 'K')
        self.assertEqual(self.card_number.get_value(), '5')
    
    def test_get_numeric_value(self):
        self.assertEqual(self.card_face.get_numeric_value(), 13)
        self.assertEqual(self.card_number.get_numeric_value(), 5)

    def test_set_original_position(self):
        self.card_face.set_original_position(x_pos=12.01, y_pos=-1.008)
        self.assertTupleEqual(self.card_face.position, (12.01, -1.008))

        self.card_number.set_original_position(x_pos=0, y_pos=0)
        self.assertTupleEqual(self.card_number.position, (0, 0))

    def test_face_up(self):
        self.assertFalse(self.card_face.is_face_up)
        self.card_face.face_up()
        self.assertTrue(self.card_face.is_face_up)