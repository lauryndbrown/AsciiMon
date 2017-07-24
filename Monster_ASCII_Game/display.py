from ascii_game.game_display.display import Display
from ascii_game.game_display.ascii_art import ASCII_Art
from ascii_game.game_display.input_tools import *
from Monster_ASCII_Game.player import MonsterGamePlayer
from Monster_ASCII_Game.monster import *
from PIL import Image
import os
import sys
import time
from colorama import init, Fore
IMAGES_DIR =  os.path.join(os.path.dirname(__file__), "Images")
import ctypes

#Player Constants
FRONT = "Front"
LEFT = "Left"
RIGHT = "Right"

#cursor methods
def move_cursor (x, y):
    print("\033[%d;%dH" % (y, x))
def move_cursor_up(lines):
    print("\033[%dA" % (lines))
def move_cursor_down(lines):
    print("\033[%dB" % (lines))
def move_cursor_forward(cols):
    print("\033[%dC" % (cols))
def move_cursor_backward(cols):
    print("\033[%dD" % (cols))
#Hide/Show cursor found at
#https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window
class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("visible", ctypes.c_byte)]
class _Coord(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short),
                ("Y", ctypes.c_short)]
def move_cursor2 (x, y):
    if os.name == 'nt':
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        coord = _Coord()
        ctypes.windll.kernel32.SetConsoleCursorPosition(handle, ctypes.byref(coord))
        old_x = coord.X
        old_y = coord.Y
        coord.X = x
        coord.Y = y
        ctypes.windll.kernel32.SetConsoleCursorPosition(handle, ctypes.byref(coord))
        return old_x, old_y
    elif os.name == 'posix':
        print("\033[%d;%dH" % (y, x))
def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        print("\033[?251", end="")

def show_cursor():
    if os.name == 'nt':    
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        print("\033[?25H", end="")
#Common Images
BLOCK_IMAGE = ["xxxx", "xxxx", "xxxx"]
FENCE_IMAGE = ["|===|===|===|", "|===|===|===|"]
GRASS_IMAGE = ["~^~^~^~^~^~^~^~^~","~^~^~^~^~^~^~^~^~","~^~^~^~^~^~^~^~~^"]
HOUSE_IMAGE = [".................__.....",
"..._____________|__|_...",
"../                  \..",
"./                    \..",
"/______________________\\",
".|        ___         |.",
".|  [ ]  |   |  [ ]   |.",
".|_______|__'|________|."]
EMPTY_IMAGE = ["    :.    "," .     :. ", ":   :.   "]    
class MonsterBattleDisplay:
    GENDER_CONVERSIONS = {Monster.FEMALE:"F", Monster.MALE:"M", Monster.GENDER_NONE:" "}
    def __init__(self):
        self.image_converter = ASCII_Art(list('#@%S?+:*,. '))
    def monster_info(self, monster):
            return "{:>23} \n HP:{:<14}]{:>3}% \n :L{} {:>18} ".format(monster.name,"="*(int(monster.health/monster.max_health*14)),int(monster.health/monster.max_health*100), monster.level, self.GENDER_CONVERSIONS[monster.gender])
    def monster_info_hp(self, monster):
        return "{:<14}".format("="*int(monster.health/monster.max_health*14))
    def monster_pic(self, monster, mon_info):
        self.image_converter.chars = list(u'#\u2593\u2592\u2591 ') 
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f8.png"))
        grass_mon =  Image.open(os.path.join(IMAGES_DIR,"b1.png"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s5.png"))
        #fire_mon = fire_mon.resize((250,250))
        #water_mon = water_mon.resize((250,250))
        #grass_mon = grass_mon.resize((250,250))
        self.image_converter.row_incr = 3
        self.image_converter.col_incr = 3
        self.image_converter.invert_chars()
        fire_mon_ascii = self.image_converter.image_to_ascii(fire_mon)
        fire_mon_ascii = self.remove_col(fire_mon_ascii, 1)
        #grass_mon = grass_mon.resize((150,150))
        grass_mon_ascii = self.image_converter.image_to_ascii(grass_mon)
        self.image_converter.row_incr = 3
        self.image_converter.col_incr = 3
        water_mon_ascii = self.image_converter.image_to_ascii(water_mon)
        combine = self.combine_str(fire_mon_ascii, mon_info)
        combine = self.combine_str(combine,water_mon_ascii)
        print(combine)
    def remove_col(self, image, col_num):
        img_ary = image.split('\n')
        for index in range(len(img_ary)):
            img_ary[index] = img_ary[index][:-col_num]
        return "\n".join(img_ary)
    def combine_str(self, str_left, str_right):
        str_left = str_left.split("\n")
        str_right = str_right.split("\n")
        for index in range(len(str_left)):
            if str_left[index]:
                str_left[index] = str_left[index]+str_right[index]+"\n"
        return "".join(str_left)
    def generate_mon_info(self, monster1, monster2):
        horizontal_border = " "*24
        mon_str1 = horizontal_border+"\n"+self.monster_info(monster1)+"\n"+horizontal_border
        mon_str2 = horizontal_border+"\n"+self.monster_info(monster2)+"\n"+horizontal_border

        tab = "\n".join(self.generate_divider("#", 25, 5))
        half_tab = "\n".join(self.generate_divider("#", 3, 5))

        mon_str1 = self.combine_str(mon_str1, tab)
        mon_str1 = self.combine_str(half_tab, mon_str1)
        mon_str2 = self.combine_str(tab, mon_str2)
        mon_str2 = self.combine_str(mon_str2, half_tab)


        top_divider = "\n".join(self.generate_divider("#", 52, 5))
        mid_divider = "\n".join(self.generate_divider("#", 52, 5))
        bottom_divider = "\n".join(self.generate_divider("#", 52, 5))
        return top_divider+"\n"+mon_str2+mid_divider+"\n"+mon_str1+bottom_divider+"\n"
        
    def generate_divider(self, char, col, lines):
        return [char*col for _ in range(lines)]
class GameMapImage:
    def __init__(self, ascii_image):
        self.ascii_image = ascii_image
        self.height = len(ascii_image)
        self.width = len(ascii_image[0])
class GameMapObject:
    def __init__(self, image, pos_x=0, pos_y=0, walkable=False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.width = image.width
        self.height = image.height
        self.walkable = walkable
class MovingMapObject(GameMapObject):
    def __init__(self, images, start_image, pos_x=0, pos_y=0):
        super().__init__(start_image, pos_x, pos_y)
        self.images = images
class GameMapPosition:
    def __init__(self, pos_x, pos_y, game_object):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.game_object = game_object
        self.walkable = game_object.walkable
class GameMap:
    EMPTY_SYMBOL = "."
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.invalid_locs = {}
        self.reset_locs = {}
        self.game_map = [list(self.EMPTY_SYMBOL*self.width) for _i in range(self.height)]
        self.objects = []
        self.player_object = None

    def render_map(self, game):
        print(self.map_to_str())

    def update_map(self, game, lines_up):
        lines_down = lines_up-self.height-1
        move_cursor_up(lines_up)
        print(self.map_to_str(), end="")
        move_cursor_down(lines_down)

    def map_to_str(self):
        game_map = []
        for i in range(len(self.game_map)):
            game_map.append("".join(self.game_map[i]))
        return "\n".join(game_map)

    def add_object(self, game_object, player=False):
        if player:
            self.player_object = game_object
        self.insert_image(game_object)
        self.objects.append(game_object)

    def insert_image(self, game_object):
        for img_x in range(game_object.image.height):
            for img_y in range(game_object.image.width):
                pos_y = game_object.pos_y+img_y
                pos_x = game_object.pos_x+img_x
                if self.game_map[pos_x][pos_y] != self.EMPTY_SYMBOL:
                    self.add_reset_loc(pos_x, pos_y)
                self.game_map[pos_x][pos_y] = game_object.image.ascii_image[img_x][img_y]
                if not game_object.walkable:
                    self.add_invalid_loc(pos_x, pos_y, game_object)

    def remove_image(self, game_object):
        for img_x in range(game_object.image.height):
            for img_y in range(game_object.image.width):
                pos_y = game_object.pos_y+img_y
                pos_x = game_object.pos_x+img_x
                self.reset_locations(pos_x, pos_y)
                if not game_object.walkable:
                    self.remove_invalid_loc(pos_x, pos_y)

    def remove_object(self, game_object):
        self.remove_image(game_object)
        self.objects.remove(game_object)
    def move_object(self, game_object, pos_x, pos_y):
        if self.check_locations(game_object, pos_x, pos_y):
            self.remove_object(game_object)
            game_object.pos_x = pos_x
            game_object.pos_y = pos_y
            self.add_object(game_object)
            return True
        return False
    def check_locations(self, game_object, pos_x, pos_y):
        for img_x in range(game_object.image.height):
            for img_y in range(game_object.image.width):
                new_y = pos_y+img_y
                new_x = pos_x+img_x
                if (new_x, new_y) in self.invalid_locs and self.invalid_locs[(new_x, new_y)].game_object!=game_object or not self.check_in_bounds(new_x, new_y):
                    return False
        return True
    def check_in_bounds(self, pos_x, pos_y):
        return pos_x >=0 and pos_x < self.height and pos_y >=0 and pos_y<self.width
    def reset_locations(self, pos_x, pos_y):
        if (pos_x, pos_y) in self.reset_locs:
            self.game_map[pos_x][pos_y] = self.reset_locs[(pos_x, pos_y)]
            self.remove_reset_loc(pos_x, pos_y)
        else:
            self.game_map[pos_x][pos_y] = self.EMPTY_SYMBOL
    def add_reset_loc(self, pos_x, pos_y):
        self.reset_locs[(pos_x, pos_y)] = self.game_map[pos_x][pos_y]
    def remove_reset_loc(self, pos_x, pos_y):
        del self.reset_locs[(pos_x, pos_y)]
    def add_invalid_loc(self, pos_x, pos_y, game_object):
        self.invalid_locs[(pos_x, pos_y)] = GameMapPosition(pos_x, pos_y, game_object)
    def remove_invalid_loc(self, pos_x, pos_y):
        del self.invalid_locs[(pos_x, pos_y)]
    def left_player_image(self):
        self.player_object.image = self.player_object.images[LEFT]
    def right_player_image(self):
        self.player_object.image = self.player_object.images[RIGHT]
    def front_player_image(self):
        self.player_object.image = self.player_object.images[FRONT]
class MonsterGameDisplay(Display):
    #White Space Offsets
    IN_GAME_MENU_OFFSET = 6
    START_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    GAME_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    BATTLE_SCREEN_OFFSET = 30 + IN_GAME_MENU_OFFSET 
    OPTION_SCREEN_OFFSET = 1 + IN_GAME_MENU_OFFSET 
    #Battle Constants
    BATTLE_START = "Battle Start"
    BATTLE_COMMANDS = "Battle Commands"
    BATTLE_SWITCH = "Battle Switch"
    BATTLE_RUN = "Battle Run"
    #Map Constants
    MAP_WIDTH = 100
    MAP_HEIGHT = 30
    def __init__(self):
        super().__init__(50)
        init()#colorama init for windows
        self.battle_display = MonsterBattleDisplay()
        self.game_map = GameMap(self.MAP_WIDTH, self.MAP_HEIGHT)
        self.map_write_pos = self.MAP_HEIGHT+ self.IN_GAME_MENU_OFFSET + 1 
        player_images = self.create_player_images()
        block_img = GameMapImage(BLOCK_IMAGE)
        fence_img = GameMapImage(FENCE_IMAGE)
        grass_img = GameMapImage(GRASS_IMAGE)
        house_img = GameMapImage(HOUSE_IMAGE)
        self.game_map.add_object(MovingMapObject(player_images, player_images[FRONT]), True)
        self.game_map.add_object(GameMapObject(fence_img, 4, 0))
        self.game_map.add_object(GameMapObject(grass_img, 20, 10, True))
        self.game_map.add_object(GameMapObject(house_img, 10, 50))

        
    def create_player_images(self):
        player_ascii_right = [u"..\u2593\u2593\u2593\u2593..",
                        ".\u2590\u2593\u2593\u2591\u2591\u2593\u2593.",
                        ".\u2593\u2592..\u2592\u2593."]
        player_ascii_left = [u"..\u2593\u2593\u2593\u2593..",
                        ".\u2593\u2591\u2591\u2593\u2593\u2593\u2593.",
                        ".\u2593\u2592..\u2592\u2593."]
        player_ascii_front = [u"..\u2593\u2593\u2593\u2593..",
                        "\u2593\u2593\u2593\u2591\u2591\u2593\u2593\u2593.",
                        ".\u2593\u2592..\u2592\u2593."]
        return {FRONT:GameMapImage(player_ascii_front),RIGHT:GameMapImage(player_ascii_right), LEFT:GameMapImage(player_ascii_left)}
    def start_menu(self, game):
        self.clear_screen()
        print(self.center("Start Screen"," "))
        title =  Image.open(os.path.join(IMAGES_DIR,"title2.png"))
        self.image_converter.row_incr = 3
        self.image_converter.col_incr = 3
        
        #self.image_converter.invert_chars()
        title_ascii = self.image_converter.image_to_ascii(title)

        print(title_ascii)
        #self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
    def game_screen(self, game, game_over=False, move=False):
        if move:
            has_moved = self.game_map.move_object(self.game_map.player_object, game.pos_x, game.pos_y)

            self.game_map.update_map(game, self.map_write_pos)
            return has_moved
        self.clear_screen()
        print(self.center("Game Screen"," "))
        #self.fill_screen(self.GAME_SCREEN_OFFSET)
        self.game_map.render_map(game)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
    def update_game_screen(self, game):
        has_moved = self.game_map.move_object(self.game_map.player_object, game.pos_x, game.pos_y)
        self.game_map.update_map(game)
        return has_moved
    def options_screen(self, game):
        self.clear_screen()
        print(self.center("Options Screen"," "))
        self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
    def battle_screen(self, game, mode, choice=None):
        self.clear_screen()
        print(self.center("Battle Screen"," "))
        self.fill_screen(self.BATTLE_SCREEN_OFFSET)
        if not mode or mode==self.BATTLE_START:
            self.display_battle_images(game)
            self._in_game_menu(game.menu)
        elif(mode==self.BATTLE_COMMANDS):
            message = self.battle_commands(game, choice)
            self.display_battle_images(game)
            if message:
                print(self.center(message," "))
                time.sleep(1)
                self.display_opponent_attack(game)
            else:
                print()
            self._in_game_menu(game.menu)
        elif(mode==self.BATTLE_SWITCH):
            self.display_battle_images(game)
            switch_menu = self.label_switch_monsters(game, game.battle.active_trainer)
            self._in_game_menu(switch_menu)
        elif(mode==self.BATTLE_RUN):
            self.display_battle_images(game)
            self.battle_run(game, game.battle.active_trainer)
        self.last_menu = (self.battle_screen, (game, mode, choice))
    def display_battle_images(self, game):
        monsters = game.battle.get_active_monsters()
        monster1_info = self.battle_display.monster_info(monsters[0])
        monster2_info = self.battle_display.monster_info(monsters[1])
        mon_info = self.battle_display.generate_mon_info(monsters[0], monsters[1])
        self.battle_display.monster_pic(monsters[0], mon_info)

    def end_screen(self):
        print(self.center("Thanks for Playing!"," "))
    def battle_commands(self, game, move):
        message = None
        if move:
            message = self.attack_message(game, move) 
        game.menu = self.label_attacks(game, game.battle.active_trainer)
        return message
    def display_opponent_attack(self, game):
        message = self.opponent_message(game)
        self.elipsis(3)
        print(self.center(message, " "), end="" )
        lines_up = 30
        lines_down = 2
        move_cursor_up(lines_up)
        self.display_battle_images(game)
        move_cursor_down(lines_down)
    def update_health_bar(self, game):
        x = 30#14
        y = 20#31
        old_x, old_y = move_cursor2(x, y)
        monster = game.battle.trainers[0].active_monster
        hp = self.battle_display.monster_info_hp(monster)
        print(hp, end="")
        move_cursor2(x,y)
    def elipsis(self, n):
        dots = []
        for i in range(n):
            dots.append(". ")
            print(self.center("".join(dots), " "), end="" )
            time.sleep(.5)
            move_cursor_up(2)
    def opponent_message(self, game):
        trainers = game.battle.trainers
        trainer1, trainer2 = trainers[0], trainers[1]
        monster1 = trainer1.active_monster
        monster2 = trainer2.active_monster
    
        move = trainer2.pick_move()
        attack_result = monster2.attack_monster(monster1, move)
        return self.create_message(monster2, monster1, move, attack_result)
    def attack_message(self, game, move):
        trainers = game.battle.trainers
        trainer1, trainer2 = trainers[0], trainers[1]
        monster1 = trainer1.active_monster
        monster2 = trainer2.active_monster
        
        attack_result = monster1.attack_monster(monster2, move)
        return self.create_message(monster1, monster2, move, attack_result)
       
    def create_message(self, monster, oppenent, move, attack_result):
        message = "{} uses {}! ".format(monster.name, move.name)
        if move.effect_type==Move.HEALTH and attack_result<0:
            message = message + "It does {} damage!".format(abs(move.max_value))
        return message
    def label_attacks(self, game, trainer):
        new_menu = []
        #append the "Back" menu option
        new_menu.append(game.menu[0])
        for move in trainer.active_monster.moves:
            new_menu.append(game.create_attack_menu_choice(move))
        return new_menu
    def label_switch_monsters(self, game, trainer):
        new_menu = []
        #append the "Back" menu option
        new_menu.append(game.menu[0])
        for monster in trainer.monsters:
            new_menu.append(game.create_switch_menu_choice(monster))
        return new_menu
    def battle_run(self, game, trainer):
        if game.battle.can_run:
                pass
        else:
            print("Cannot Run")
            time.sleep(5)
            
if __name__=="__main__":
    init()
    print(Fore.RED+"red text")
    print("a\nb\nc\n", end="e")
    move_cursor_up(3)
    print("h")
    move_cursor_down(3)
    print("z")
