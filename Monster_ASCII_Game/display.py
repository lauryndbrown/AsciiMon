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
            return "{:>22} \nHP:{:>17}] \n:L{} {:>18} ".format(monster.name,"="*(monster.health//monster.max_health*18), monster.level, self.GENDER_CONVERSIONS[monster.gender])
    def monster_pic(self, monster, mon_info):
        self.image_converter.chars = list(u'\u2593\u2592\u2591#@%SZ+:,. ')#-- very good!
        #self.image_converter.chars = list(u'\u2593\u2592\u2591:. ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2593\u2592\u2591:. ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2590\u2593\u2592\u2591/ ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2590\u2593\u2592\u2591|* ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2590\u2593\u2592\u2591\u2580| ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2590\u2593\u2592\u2591| ') #---AMAZING!
        self.image_converter.chars = list(u'\u2580\u2590\u2593\u2592\u2591 ') #---AMAZING!
        self.image_converter.chars = list(u'#\u2593\u2592\u2591 ') #---AMAZING!
        #self.image_converter.invert_chars()
        #image = Image.open(os.path.join(self.IMAGES,"verticle_line.png"))
        #title_image = self.image_converter.scale_image(title_image, 400)
       # o_image = o_image.resize((50,25))
        #self.ascii_x = self.image_converter.image_to_ascii(x_image)
        #fire_mon =  Image.open(os.path.join(IMAGES_DIR,"charmander1.jpg"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"charmander2.png"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f1.png"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f5.png"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f6.png"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f7.png"))
        fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f8.png"))
        #fire_mon =  Image.open(os.path.join(IMAGES_DIR,"f3.png"))
        #fire_mon =  Image.open(os.path.join(IMAGES_DIR,"charmander3.png"))
        #fire_mon =  Image.open(os.path.join(IMAGES_DIR,"250px-004Charmander.png"))
        grass_mon =  Image.open(os.path.join(IMAGES_DIR,"b1.png"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s1.gif"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s2.png"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s3.png"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s4.png"))
        water_mon =  Image.open(os.path.join(IMAGES_DIR,"s5.png"))
        #fire_mon = fire_mon.resize((250,250))
        #water_mon = water_mon.resize((250,250))
        #grass_mon = grass_mon.resize((250,250))
       # fire_mon.show()
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
        print(fire_mon_ascii)
        print(grass_mon_ascii)
        print(water_mon_ascii)
     #   combine_img = self.image_converter.combine(fire_mon_ascii, water_mon_ascii)
    #    combine_img = self.image_converter.combine(fire_mon_ascii, divider)
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
        print("Right: ",len(str_right),"Left: ",len(str_left))
        for index in range(len(str_left)):
            if str_left[index]:
                str_left[index] = str_left[index]+str_right[index]+"\n"
        return "".join(str_left)
    def generate_mon_info(self, monster1, monster2):
        horizontal_border = " "*23
        mon_str1 = horizontal_border+"\n"+self.monster_info(monster1)+"\n"+horizontal_border
        mon_str2 = horizontal_border+"\n"+self.monster_info(monster2)+"\n"+horizontal_border

        tab = "\n".join(self.generate_divider("#", 25, 5))
        half_tab = "\n".join(self.generate_divider("#", 2, 5))

        mon_str1 = self.combine_str(mon_str1, tab)
        mon_str1 = self.combine_str(half_tab, mon_str1)
        mon_str2 = self.combine_str(tab, mon_str2)
        mon_str2 = self.combine_str(mon_str2, half_tab)


        top_divider = "\n".join(self.generate_divider("#", 50, 5))
        mid_divider = "\n".join(self.generate_divider("#", 50, 5))
        bottom_divider = "\n".join(self.generate_divider("#", 50, 5))
        return top_divider+"\n"+mon_str2+mid_divider+"\n"+mon_str1+bottom_divider+"\n"
        
    def generate_divider(self, char, col, lines):
        return [char*col for _ in range(lines)]
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
        if not mode or mode==self.BATTLE_START:
            self.display_battle_images(game)
            self._in_game_menu(game.menu)
        elif(mode==self.BATTLE_COMMANDS):
            message = self.battle_commands(game, choice)
            self.display_battle_images(game)
            if message:
                print(self.center(message," "))
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

