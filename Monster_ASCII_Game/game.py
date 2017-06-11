from ascii_game.game import Game, Choice
from Monster_ASCII_Game.display import MonsterGameDisplay
from Monster_ASCII_Game.player import MonsterGamePlayer


class MonsterGame(Game):
    #Menu Names
    START_MENU_NAME = "Start"
    GAME_MENU_NAME = "Game"
    OPTIONS_MENU_NAME = "Options"

    def __init__(self, display, player1):
        super().__init__(display, player1, None)
        self._set_up_menus()
    def _set_up_menus(self):
        start_menu = []
        game_menu = []
        options_menu = []
        #Start Menu Choices
        start_menu.append(Choice("Start Game", self.display.game_screen, (self,), self.GAME_MENU_NAME))
        start_menu.append(Choice("Exit Monster Game", self.end_game, None, None))
        #Game Menu Choices
        game_menu.append(Choice("Options Menu", self.options_screen, (), self.OPTIONS_MENU_NAME))
        #Option Menu Choices
        options_menu.append(Choice("Resume Game", self.display.game_screen, (self,), self.GAME_MENU_NAME))
        options_menu.append(Choice("End Current Game", self.end_current_game, (), self.START_MENU_NAME))
        
        self.menus = {self.START_MENU_NAME:start_menu, self.GAME_MENU_NAME:game_menu, self.OPTIONS_MENU_NAME:options_menu}
        self.menu = start_menu
        self.prev_menu = None
    def start(self):
        self.display.start_menu(self)
        super().start()
    def end_game(self):
        self.display.end_screen()
    def options_screen(self):
        self.display.options_screen(self)
    def end_current_game(self):
        self.create_new_game()
        self.display.start_menu(self)
    def create_new_game(self):
        pass
    def get_battle_command(self, trainer):
       return self.display.battle_commands(self, trainer)
    def get_switch_monster(self, trainer):
       return self.display.switch_monster(self, trainer)

if __name__=="__main__":
    display = MonsterGameDisplay()
    player = MonsterGamePlayer("Ash")
    game = MonsterGame(display, player)
    game.start()
