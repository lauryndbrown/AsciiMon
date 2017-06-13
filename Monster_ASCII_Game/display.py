from ascii_game.game_display.display import Display
from ascii_game.game_display.ascii_art import ASCII_Art
from ascii_game.game_display.input_tools import *
from Monster_ASCII_Game.player import MonsterGamePlayer
from Monster_ASCII_Game.monster import *
from PIL import Image
import os
import time
IMAGES_DIR = os.path.join("Monster_ASCII_Game", "Images")

class MonsterBattleDisplay:
    GENDER_CONVERSIONS = {Monster.FEMALE:"F", Monster.MALE:"M", Monster.GENDER_NONE:" "}
    def __init__(self):
        self.image_converter = ASCII_Art(list('#@%S?+:*,. '))
    def monster_info(self, monster):
            return "{:>23} \n HP:{:<14}]{:>3}% \n :L{} {:>18} ".format(monster.name,"="*(int(monster.health/monster.max_health*14)),int(monster.health/monster.max_health*100), monster.level, self.GENDER_CONVERSIONS[monster.gender])
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
    def __init__(self, image, pos_x=0, pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.width = image.width
        self.height = image.height
class GameMap:
    EMPTY_SYMBOL = "#"
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.invalid_locs = []
        self.game_map = [list(self.EMPTY_SYMBOL*self.width) for _i in range(self.height)]
        self.objects = []
        self.player_object = None
    def render_map(self, game):
        print(self.map_to_str())
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
                self.game_map[pos_x][pos_y] = game_object.image.ascii_image[img_x][img_y]
                self.add_invalid_loc(pos_x, pos_y)
    def remove_image(self, game_object):
        for img_x in range(game_object.image.height):
            for img_y in range(game_object.image.width):
                pos_y = game_object.pos_y+img_y
                pos_x = game_object.pos_x+img_x
                self.game_map[pos_x][pos_y] = self.EMPTY_SYMBOL
                self.remove_invalid_loc(pos_x, pos_y)

    def remove_object(self, game_object):
        self.remove_image(game_object)
        self.objects.remove(game_object)
    def move_object(self, game_object, pos_x, pos_y):
        if (pos_x, pos_y) not in self.invalid_locs:
            self.remove_object(game_object)
            game_object.pos_x = pos_x
            game_object.pos_y = pos_y
            self.add_object(game_object)
            return True
        return False
    def add_invalid_loc(self, pos_x, pos_y):
        self.invalid_locs.append((pos_x, pos_y))
    def remove_invalid_loc(self, pos_x, pos_y):
        self.invalid_locs.remove((pos_x, pos_y))
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
    MAP_WIDTH = 10#100
    MAP_HEIGHT = 5#30
    
    def __init__(self):
        super().__init__(50)
        self.battle_display = MonsterBattleDisplay()
        self.game_map = GameMap(self.MAP_WIDTH, self.MAP_HEIGHT)
        player_img = GameMapImage([["?"]])
        block_img = GameMapImage(["xxxx", "yyyy"])
        self.game_map.add_object(GameMapObject(player_img), True)
        self.game_map.add_object(GameMapObject(block_img, 1, 0))
    def start_menu(self, game):
        self.clear_screen()
        print(self.center("Start Screen"," "))
        self.fill_screen(self.GAME_SCREEN_OFFSET)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
    def game_screen(self, game, game_over=False):
        self.clear_screen()
        print(self.center("Game Screen"," "))
        #self.fill_screen(self.GAME_SCREEN_OFFSET)
        has_moved = self.game_map.move_object(self.game_map.player_object, game.pos_x, game.pos_y)
        self.game_map.render_map(game)
        self._in_game_menu(game.menu)
        self.last_menu = (self.game_screen, (game, ))
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
    def attack_message(self, game, move):
        trainers = game.battle.trainers
        trainer1, trainer2 = trainers[0], trainers[1]
        monster1 = trainer1.active_monster
        monster2 = trainer2.active_monster
        
        attack_result = monster1.attack_monster(monster2, move)
        
        message = "{} uses {}! ".format(monster1.name, move.name)
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
    battle = MonsterBattleDisplay()
    monster1 = Monster("Monster", "N", 7, "Ami")
    monster2 = Monster("Monster", "F")

