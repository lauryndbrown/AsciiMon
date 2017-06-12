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
    def battle_screen(self, game, mode, choice=None):
        self.clear_screen()
        print(self.center("Battle Screen"," "))
        self.fill_screen(self.BATTLE_SCREEN_OFFSET)
        monsters = game.battle.get_active_monsters()
        monster1_info = self.battle_display.monster_info(monsters[0])
        monster2_info = self.battle_display.monster_info(monsters[1])
        print(monster2_info)
        print(monster1_info)
        if not mode or mode==self.BATTLE_START:
            print("MODE:", mode)
            self._in_game_menu(game.menu)
        elif(mode==self.BATTLE_COMMANDS):
            self.battle_commands(game, choice)
        elif(mode==self.BATTLE_SWITCH):
            switch_menu = self.label_switch_monsters(game, game.battle.active_trainer)
            self._in_game_menu(switch_menu)
        elif(mode==self.BATTLE_RUN):
            self.battle_run(game, game.battle.active_trainer)
        self.last_menu = (self.battle_screen, (game, mode, choice))

    def end_screen(self):
        print(self.center("Thanks for Playing!"," "))
    def battle_commands(self, game, move):
        if move:
            trainers = game.battle.trainers
            trainer1, trainer2 = trainers[0], trainers[1]
           
            monster1 = trainer1.active_monster
            monster2 = trainer2.active_monster
            print("Choice:{} Moves:{}".format(move, monster1.moves))
            monster1.attack_monster(monster2, move)
        game.menu = self.label_attacks(game, game.battle.active_trainer)
        self._in_game_menu(game.menu)
    def label_attacks(self, game, trainer):
        new_menu = []
        #append the "Back" menu option
        new_menu.append(game.menu[0])
        for move in trainer.active_monster.moves:
            new_menu.append(game.create_attack_menu_choice(move))
        print("NEW MENU:", new_menu)
        return new_menu
    def label_switch_monsters(self, game, trainer):
        new_menu = []
        #append the "Back" menu option
        new_menu.append(game.menu[0])
        for monster in trainer.monsters:
            new_menu.append(game.create_switch_menu_choice(monster))
        print("NEW MENU:", new_menu)
        return new_menu


if __name__=="__main__":
    battle = MonsterBattleDisplay()
    monster1 = Monster("Monster", "N", 7, "Ami")
    monster2 = Monster("Monster", "F")

