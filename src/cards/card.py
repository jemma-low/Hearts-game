import arcade
from constants.card import CARD_CLICK_UP_CHANGE, FACE_VALUES, FACE_DOWN_IMAGE


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit: str, value: str, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit: str = suit
        self.value: str = value
        self.numeric_value: int = -1

        # Need to convert face cards to numeric value
        if value in FACE_VALUES.keys():
            self.numeric_value = FACE_VALUES[value]
        else:
            self.numeric_value = int(value)

        self.x_pos_original: float = 0
        self.y_pos_original: float = 0

        self.original_index: int = -1

        # Image to use for the sprite when face up
        self.image_file_name: str = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        self.image_face_down: str = FACE_DOWN_IMAGE

        # Call the parent
        super().__init__(self.image_face_down, scale, hit_box_algorithm="None")

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True
    
    def set_original_position(self, x_pos: float, y_pos: float):
        self.x_pos_original = x_pos
        self.y_pos_original = y_pos
        self.position = x_pos, y_pos
    
    def get_original_index(self) -> int:
        return self.original_index

    def set_original_index(self, index: int):
        self.original_index = index

    def click_passing(self):
        self.set_position(self.center_x, self.center_y+CARD_CLICK_UP_CHANGE)
    
    def get_suit(self) -> str:
        return self.suit
    
    def get_value(self) -> str:
        return self.value
    
    def get_numeric_value(self) -> int:
        return self.numeric_value

    def is_suit(self, suit: str) -> bool:
        return self.suit == suit
    
    def print_card(self):
        print(f'Card:{self.value}{self.suit}')
    
    def get_card_formatted(self) -> str:
        return f'{self.value}{self.suit}'

    # TODO modify for passing
    def reset(self):
        self.set_position(self.x_pos_original, self.y_pos_original)
        self.clicks = 0


