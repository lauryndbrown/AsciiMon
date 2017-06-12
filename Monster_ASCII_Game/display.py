from ascii_game.game_display.display import Display
from ascii_game.game_display.input_tools import *
from Monster_ASCII_Game.player import MonsterGamePlayer
from Monster_ASCII_Game.monster import Monster
from PIL import Image
import os
IMAGES_DIR = os.path.join("Monster_ASCII_Game", "Images")

class MonsterBattleDisplay:
    GENDER_CONVERSIONS = {Monster.FEMALE:"F", Monster.MALE:"M", Monster.GENDER_NONE:" "}
    def monster_info(self, monster):
        return "{}\n:L{} {}".format(monster.name, monster.level, self.GENDER_CONVERSIONS[monster.gender])
class MonsterGameDisplay(Display):
    #White Space Offsets
    IN_GAME_MENU_OFFSET = 6
    START_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    GAME_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    BATTLE_SCREEN_OFFSET = 7 + IN_GAME_MENU_OFFSET 
    OPTION_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    #Battle Constants
    BATTLE_START = "Battle Start"
    BATTLE_COMMANDS = "Battle Commands"
    BATTLE_SWITCH = "Battle Switch"
    BATTLE_RUN = "Battle Run"
    def __init__(self):
        super().__init__(50)
        self.battle_display = MonsterBattleDisplay()
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
    def battle_screen(self, game, mode):
        self.clear_screen()
        print(self.center("Battle Screen"," "))
        self.fill_screen(self.BATTLE_SCREEN_OFFSET)
        monsters = game.battle.get_active_monsters()
        monster1_info = self.battle_display.monster_info(monsters[0])
        monster2_info = self.battle_display.monster_info(monsters[1])
        print(monster2_info)
        print(monster1_info)
        if not mode or mode==self.BATTLE_START:
            self._in_game_menu(game.menu)
            self.last_menu = (self.battle_screen, (game, mode))
        elif(mode==self.BATTLE_COMMANDS):
            attack_menu = self.label_attacks(game, game.battle.active_trainer)
            self._in_game_menu(attack_menu)
            self.last_menu = (self.battle_screen, (game, mode))
        elif(mode==self.BATTLE_SWITCH):
            self.battle_switch(game, game.battle.active_trainer)
        elif(mode==self.BATTLE_RUN):
            self.battle_run(game, game.battle.active_trainer)

    def end_screen(self):
        print(self.center("Thanks for Playing!"," "))
    def label_attacks(self, game, trainer):
        new_menu = list(game.menu)
        moves = trainer.active_monster.moves
        for index in range(len(moves)):
            new_menu[index] = moves[index]
        return new_menu

if __name__=="__main__":
    battle = MonsterBattleDisplay()
    monster1 = Monster("Monster", "N", 7, "Ami")
    monster2 = Monster("Monster", "F")

