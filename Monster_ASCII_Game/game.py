from ascii_game.game import Game, Choice
from Monster_ASCII_Game.display import MonsterGameDisplay, hide_cursor, show_cursor
from Monster_ASCII_Game.player import MonsterGamePlayer
from Monster_ASCII_Game.battle import Battle, create_trainers
from msvcrt import getch


#Move Constants
MOVE_LEFT = "Left"
MOVE_RIGHT = "Right"
MOVE_UP = "Up"
MOVE_DOWN = "Down"

ESC = 27
ENTER = 13
SPACE = 32
SPECIAL_KEYS = 224
DOWN_ARROW = 80
UP_ARROW = 72
LEFT_ARROW = 75
RIGHT_ARROW = 77
class MonsterGame(Game):
    #Menu Names
    START_MENU_NAME = "Start"
    GAME_MENU_NAME = "Game"
    MOVE_MENU_NAME = "Move Mode"
    BATTLE_MENU_NAME = "Battle"
    BATTLE_ATTACK_MENU_NAME = "Battle Attack"
    BATTLE_SWITCH_MENU_NAME = "Battle Switch"
    OPTIONS_MENU_NAME = "Options"
    #Common Menu Constants
    BACK_OPTION = "Back"
    #Battle Constants
    BATTLE_START = "Battle Start"
    BATTLE_ATTACK = "Battle Attack"
    BATTLE_SWITCH = "Battle Switch"
    BATTLE_RUN = "Battle Run"
    BATTLE_NEW = "Battle New"
    #DIRECTIONS = {MOVE_LEFT:-10, MOVE_RIGHT:10, MOVE_UP:-3, MOVE_DOWN:3}
    DIRECTIONS = {MOVE_LEFT:-1, MOVE_RIGHT:1, MOVE_UP:-1, MOVE_DOWN:1}

    def __init__(self, display, player1):
        super().__init__(display, player1, None)
        self._set_up_menus()
        self.pos_x = 0
        self.pos_y = 0
    def _set_up_menus(self):
        start_menu = []
        game_menu = []
        move_menu = []
        battle_menu = []
        battle_attack_menu = []
        battle_switch_menu = []
        options_menu = []
        #Start Menu Choices
        start_menu.append(Choice("Start Game", self.display.game_screen, (self,), self.GAME_MENU_NAME))
        start_menu.append(Choice("Exit Monster Game", self.end_game, None, None))
        #Game Menu Choices
        game_menu.append(Choice("Battle", self.battle_screen, (self.BATTLE_NEW, ), self.BATTLE_MENU_NAME))
        game_menu.append(Choice("Options Menu", self.options_screen, (), self.OPTIONS_MENU_NAME))
        game_menu.append(Choice("Move Mode", self.move_keypress, (), None))
        #Move Menu Choices
        move_menu.append(Choice("ESC", None, ( ), None))
        move_menu.append(Choice("Left", None, ( ), None))
        move_menu.append(Choice("Right", None, ( ), None))
        move_menu.append(Choice("Up", None, ( ), None))
        move_menu.append(Choice("Down", None, ( ), None))
        #Battle Menu Choices
        battle_menu.append(Choice("Attack", self.battle_screen, (self.BATTLE_ATTACK, ), self.BATTLE_ATTACK_MENU_NAME))
        #battle_menu.append(Choice("Switch", self.battle_screen, (self.BATTLE_SWITCH, ), self.BATTLE_SWITCH_MENU_NAME))
        battle_menu.append(Choice("Options Menu", self.options_screen, (), self.OPTIONS_MENU_NAME))
#        battle_menu.append(Choice("Run", self.battle_screen, (self.BATTLE_RUN, ), None))
        #Battle Menu Choices
        battle_attack_menu.append(Choice(self.BACK_OPTION, self.battle_screen, None, self.BATTLE_MENU_NAME))
        #Battle Switch Choices
        battle_switch_menu.append(Choice(self.BACK_OPTION, self.battle_screen, None, self.BATTLE_MENU_NAME))
        #Option Menu Choices
        options_menu.append(Choice("Resume Game", self.display.game_screen, (self,), self.GAME_MENU_NAME))
        options_menu.append(Choice("End Current Game", self.end_current_game, (), self.START_MENU_NAME))
        
        self.menus = {self.START_MENU_NAME:start_menu, self.GAME_MENU_NAME:game_menu, self.OPTIONS_MENU_NAME:options_menu, self.BATTLE_MENU_NAME:battle_menu, self.BATTLE_ATTACK_MENU_NAME:battle_attack_menu, self.BATTLE_SWITCH_MENU_NAME:battle_switch_menu, self.MOVE_MENU_NAME:move_menu }
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
    def move_keypress(self):
        print("Arrow Keys to Move or Esc to go Back")
        hide_cursor()
        while True:
            key = ord(getch())
            if key == ESC:
                break
            elif key==SPECIAL_KEYS:
                key = ord(getch())
                if key==DOWN_ARROW:
                    self.move(MOVE_DOWN)
                elif key==UP_ARROW:
                    self.move(MOVE_UP)
                elif key==RIGHT_ARROW:
                    self.move(MOVE_RIGHT)
                elif key==LEFT_ARROW:
                    self.move(MOVE_LEFT)
        show_cursor()
    def move(self, direction):
        direction_value = self.DIRECTIONS[direction]
        old_x = self.pos_x
        old_y = self.pos_y
        if direction==MOVE_LEFT and self.pos_y+direction_value>=0:
            self.pos_y += direction_value
            self.display.game_map.left_player_image()
        elif direction==MOVE_RIGHT and self.pos_y+direction_value<self.display.MAP_WIDTH:
            self.pos_y += direction_value
            self.display.game_map.right_player_image()
        elif direction==MOVE_DOWN and self.pos_x+direction_value<self.display.MAP_HEIGHT:
            self.pos_x += direction_value
            self.display.game_map.front_player_image()
        elif direction==MOVE_UP and self.pos_x+direction_value>=0:
            self.pos_x += direction_value
            self.display.game_map.front_player_image()
        has_moved = self.display.game_screen(self, False, True)
        if not has_moved:
            self.pos_x = old_x
            self.pos_y = old_y
    def battle_screen(self, flag=None, choice=None):
        if not flag:
            self.display.battle_screen(self, None)
        elif flag==self.BATTLE_NEW:
            player_trainer, ai_trainer, wild_trainer = create_trainers(game)
            self.new_battle(player_trainer, ai_trainer)
        elif flag==self.BATTLE_ATTACK:
            self.display.battle_screen(self, self.display.BATTLE_COMMANDS, choice)
        elif flag==self.BATTLE_SWITCH:
            self.display.battle_screen(self, self.display.BATTLE_SWITCH, choice)
        elif flag==self.BATTLE_RUN:
            self.display.battle_screen(self, self.display.BATTLE_RUN)

    def new_battle(self, trainer1, trainer2):
        print("new battle")
        self.battle = Battle([trainer1, trainer2])
        self.display.battle_screen(self, MonsterGameDisplay.BATTLE_START)
        self.battle.reset_active_monsters()
    def get_battle_command(self, trainer):
       return self.display.battle_commands(self, trainer)
    def get_switch_monster(self, trainer):
       return self.display.switch_monster(self, trainer)
    def create_attack_menu_choice(self, move):
       return Choice(move.name, self.battle_screen, (self.BATTLE_ATTACK, move ), self.BATTLE_ATTACK_MENU_NAME)
    def create_switch_menu_choice(self, monster):
       return Choice(monster.name, self.battle_screen, (self.BATTLE_SWITCH, monster ), self.BATTLE_SWITCH_MENU_NAME)
def start():
    display = MonsterGameDisplay()
    player = MonsterGamePlayer("Ash")
    game = MonsterGame(display, player)
    game.start()

if __name__=="__main__":
    start()
