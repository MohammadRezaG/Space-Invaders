from games import *
from load import *
if __name__ == '__main__':
    setings = Setings.load_setings()
    assets = Assets(setings)
    game = Game(
        setings, assets, 
    800, 600)
    game.start_game()