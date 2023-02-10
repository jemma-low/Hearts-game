from game import *
import sys


def main():
    """ Main function """
    window = Game()
    is_debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1]
        if debug.strip() == '--debug':
            is_debug = True
    window.setup(is_debug)
    arcade.run()

if __name__ == "__main__":
    main()