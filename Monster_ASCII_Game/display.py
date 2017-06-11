from ascii_game.game_display.display import Display
from ascii_game.game_display.input_tools import *
from Monster_ASCII_Game.player import MonsterGamePlayer
from PIL import Image
import os

class MonsterGameDisplay(Display):
    IMAGES_DIR = os.path.join("Monster_ASCII_Game", "Images")
    #White Space Offsets
    IN_GAME_MENU_OFFSET = 6
    START_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    GAME_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    OPTION_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 

    def __init__(self):
        super().__init__(50)
    def start_menu(self, game):
        self.clear_screen()
        print(self.center("Start Screen"," "))
        self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
    def game_screen(self, game, game_over=False):
        self.clear_screen()
        print(self.center("Game Screen"," "))
        self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game))
    def options_screen(self, game):
        self.clear_screen()
        print(self.center("Options Screen"," "))
        self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game))
    def end_screen(self):
        print(self.center("Thanks for Playing!"," "))

