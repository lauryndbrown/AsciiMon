from abc import ABC, abstractmethod
from Monster_ASCII_Game.game import MonsterGame
import random
class Trainer:
    FAINTED = "Fainted"
    def __init__(self, monsters, prize_money):
        self.monsters = monsters
        self.active_monster = monsters[0]
        if(not prize_money):
            self.prize_money = 100
        else:
            self.prize_money = prize_money
    def decide(self, active_monsters):
        return self.attack()
    def pick_move(self):
        return random.choice(self.active_monster.moves)
    def pick_target(self, active_monsters):
        for monster in active_monsters:
            if monster != self.active_monster:
                return monster
    def attack(self, active_monsters):
        target = self.pick_target(active_monsters)
        move = self.pick_move()
        self.active_monster.attack(target, move)
        if(target.health<=0):
            return self.FAINTED
    def has_healthy_monsters(self):
        for monster in self.monsters:
            if monster.health>0:
                return True
        return False
class Wild_Trainer(Trainer):
    def __init__(self, monsters, prize_money=0):
        super().__init__(monsters, prize_money)

class Player_Trainer(Trainer):
    ATTACK = "Attack"
    SWITCH = "Swtich"
    ITEM = "Item"
    def __init__(self, name, game, monsters, prize_money):
        super().__init__(monsters, prize_money)
        self.name = name
        self.game = game
    def switch_monster(self, monster):
        self.active_monster = monster
    def decide(self, active_monsters):
        choice = self.ask_for_choice()
        if(choice==self.ATTACK):
            self.attack(active_monsters)
        else if(choice==self.SWITCH):
            self.switch(self.ask_for_switch())
        return choice
    def get_battle_command(self):
        return self.game.get_battle_command(self)
    def get_switch_monster(self):
        return self.game.get_switch_monster(self)
class AI_Trainer(Player_Trainer):
    def __init__(self, name, game, monsters):
        super().__init__(name, game, monsters, prize_money)
    def get_battle_command(self):
        return self.ATTACK
    def get_switch_monster(self):
        for monster in self.monsters:
            if monster.health>0:
                return monster
    
