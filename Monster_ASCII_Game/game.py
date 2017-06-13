from ascii_game.game import Game, Choice
from Monster_ASCII_Game.display import MonsterGameDisplay
from Monster_ASCII_Game.player import MonsterGamePlayer
from Monster_ASCII_Game.battle import Battle, create_trainers


#Move Constants
MOVE_LEFT = "Left"
MOVE_RIGHT = "Right"
MOVE_UP = "Up"
MOVE_DOWN = "Down"

class MonsterGame(Game):
    #Menu Names
    START_MENU_NAME = "Start"
    GAME_MENU_NAME = "Game"
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
    DIRECTIONS = {MOVE_LEFT:-10, MOVE_RIGHT:10, MOVE_UP:-3, MOVE_DOWN:3}

    def __init__(self, display, player1):
        super().__init__(display, player1, None)
        self._set_up_menus()
        self.pos_x = 0
        self.pos_y = 0
    def _set_up_menus(self):
        start_menu = []
        game_menu = []
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
        game_menu.append(Choice("Move Left", self.move, (MOVE_LEFT, ), None))
        game_menu.append(Choice("Move Right", self.move, (MOVE_RIGHT, ), None))
        game_menu.append(Choice("Move Up", self.move, (MOVE_UP, ), None))
        game_menu.append(Choice("Move Down", self.move, (MOVE_DOWN, ), None))
        #Battle Menu Choices
        battle_menu.append(Choice("Attack", self.battle_screen, (self.BATTLE_ATTACK, ), self.BATTLE_ATTACK_MENU_NAME))
        battle_menu.append(Choice("Switch", self.battle_screen, (self.BATTLE_SWITCH, ), self.BATTLE_SWITCH_MENU_NAME))
#        battle_menu.append(Choice("Run", self.battle_screen, (self.BATTLE_RUN, ), None))
        #Battle Menu Choices
        battle_attack_menu.append(Choice(self.BACK_OPTION, self.battle_screen, None, self.BATTLE_MENU_NAME))
        #Battle Switch Choices
        battle_switch_menu.append(Choice(self.BACK_OPTION, self.battle_screen, None, self.BATTLE_MENU_NAME))
        #Option Menu Choices
        options_menu.append(Choice("Resume Game", self.display.game_screen, (self,), self.GAME_MENU_NAME))
        options_menu.append(Choice("End Current Game", self.end_current_game, (), self.START_MENU_NAME))
        
        self.menus = {self.START_MENU_NAME:start_menu, self.GAME_MENU_NAME:game_menu, self.OPTIONS_MENU_NAME:options_menu, self.BATTLE_MENU_NAME:battle_menu, self.BATTLE_ATTACK_MENU_NAME:battle_attack_menu, self.BATTLE_SWITCH_MENU_NAME:battle_switch_menu }
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
    def move(self, direction):
        direction_value = self.DIRECTIONS[direction]
        old_x = game.pos_x
        old_y = game.pos_y
        if direction==MOVE_LEFT and game.pos_y+direction_value>=0:
            game.pos_y += direction_value
            game.display.game_map.left_player_image()
            print("Left")
        elif direction==MOVE_RIGHT and game.pos_y+direction_value<game.display.MAP_WIDTH:
            game.pos_y += direction_value
            game.display.game_map.right_player_image()
            print("Right")
        elif direction==MOVE_DOWN and game.pos_x+direction_value<game.display.MAP_HEIGHT:
            game.pos_x += direction_value
            game.display.game_map.front_player_image()
            print("Down")
        elif direction==MOVE_UP and game.pos_x+direction_value>=0:
            game.pos_x += direction_value
            game.display.game_map.front_player_image()
            print("Up")
        else:
            print("invalid move")
        print("({},{})".format(game.pos_x, game.pos_y))
        has_moved = self.display.game_screen(self)
        if not has_moved:
            game.pos_x = old_x
            game.pos_y = old_y
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
if __name__=="__main__":
    display = MonsterGameDisplay()
    player = MonsterGamePlayer("Ash")
    game = MonsterGame(display, player)
    game.start()
