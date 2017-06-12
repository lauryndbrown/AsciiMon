from Monster_ASCII_Game.trainer import Trainer, Wild_Trainer, Player_Trainer, AI_Trainer
from Monster_ASCII_Game.display import *
from Monster_ASCII_Game.monster import *

class Battle:
    DRAW = "Draw"
    NO_WINNER_YET = "No Winner Yet"
    def __init__(self, trainers, can_run=False):
        if(len(trainers)>=2):
            self.trainers = trainers
        else:
            raise ValueError("Battle requires at least 2 trainers")
        self.winner = self.NO_WINNER_YET
        self.reset_active_monsters()
        self.active_trainer = trainers[0]
        self.can_run = can_run
    def start(self):
        while(self.winner==self.NO_WINNER_YET):
            self.trainer_turns()
        self.reset_active_monsters()
    def reset_active_monsters(self):
        for trainer in self.trainers:
            trainer.reset_active_monster()
    def get_active_monsters(self):
        return [trainer.active_monster for trainer in self.trainers]

    def trainer_turns(self):
        active_monsters = self.get_active_monsters()
        for trainer in self.trainers:
            self.active_trainer = trainer
            has_fainted = trainer.decide(active_monsters)
            if(has_fainted==Trainer.FAINTED):
                self.winner = self.check_winner()
            if(self.winner!=self.NO_WINNER_YET):
                break
    def check_winner(self):
        #For Now assume trainers == 2!!!
        trainer1 = trainers[0].has_healthy_monsters()
        trainer2 = trainers[1].has_healthy_monsters()
        if(not trainer1 and not trainer2):
            return self.DRAW
        if(not trainer1):
            return trainer2
        if(not trainer2):
            return trainer1
        return self.NO_WINNER_YET
        return trainer1
#Methods for Debugging
def create_monster_species():
    weakness_mult = 2
    resistence_mult = .5

    water_type = Element_Type("Water") 
    fire_type = Element_Type("Fire") 
    grass_type = Element_Type("Grass")
    normal_type = Element_Type("Normal")

    types = [water_type, fire_type, grass_type, normal_type]
    #Weaknesses
    water_type.weaknesses=[Type_Difference(grass_type, weakness_mult)]
    fire_type.weaknesses=[Type_Difference(water_type, weakness_mult)]
    grass_type.weaknesses=[Type_Difference(fire_type, weakness_mult)]
    #Resistences
    water_type.resistences = [Type_Difference(fire_type, resistence_mult)]
    fire_type.resistences =  [Type_Difference(grass_type, resistence_mult)]
    grass_type.resistences =  [Type_Difference(water_type, resistence_mult)]

    scratch = Move("Scratch", Move.HEALTH, normal_type, -30)
    tackle = Move("Tackle", Move.HEALTH, normal_type, -20)
    tail_whip = Move("Tail Whip", Move.DEFENSE, normal_type, -20)
    growl = Move("Growl", Move.ATTACK, normal_type, -20)
    ember = Move("Ember", Move.HEALTH, fire_type, -30)
    bubble = Move("Bubble", Move.HEALTH, water_type, -20)
    vine_whip = Move("Vine Whip", Move.HEALTH, grass_type, -20)
    attacks = [scratch, tackle, tail_whip, growl, ember, bubble, vine_whip]


    experience_mult = 3.5
    fire_mon_moves = {1:scratch,2:tail_whip,7:ember}
    fire_mon_health = {5:100, 6:110, 7:125}
    fire_mon_speed = {5:5, 6:6, 7:7}
    fire_mon_attack = {5:6, 6:7, 7:9}
    fire_mon_defense = {5:5, 6:6, 7:7}
    fire_mon_species = Species("Fire Mon", fire_type, fire_mon_moves,fire_mon_health, fire_mon_speed, fire_mon_attack, fire_mon_defense, experience_mult)

    water_mon_moves = {1:tackle,2:growl,7:bubble}
    water_mon_health = {5:100, 6:110, 7:125}
    water_mon_speed = {5:6, 6:7, 7:9}
    water_mon_attack = {5:5, 6:6, 7:7}
    water_mon_defense = {5:5, 6:6, 7:7}
    water_mon_species = Species("Water Mon", water_type, water_mon_moves, water_mon_health,water_mon_speed, water_mon_attack, water_mon_defense, experience_mult)

    grass_mon_moves = {1:tackle,2:tail_whip,7:vine_whip}
    grass_mon_health = {5:100, 6:125, 7:150}
    grass_mon_speed = {5:5, 6:5, 7:6}
    grass_mon_attack = {5:5, 6:6, 7:7}
    grass_mon_defense = {5:6, 6:7, 7:9}
    grass_mon_species = Species("Grass Mon", grass_type, grass_mon_moves,grass_mon_health, grass_mon_speed, grass_mon_attack, grass_mon_defense, experience_mult)

    return grass_mon_species, fire_mon_species, water_mon_species

def create_trainers(game):
    grass_mon_species, fire_mon_species, water_mon_species = create_monster_species() 
    grass_mon = Monster(grass_mon_species, Monster.FEMALE)
    grass_mon_2 = Monster(grass_mon_species, Monster.MALE)
    fire_mon = Monster(fire_mon_species, Monster.MALE)
    water_mon = Monster(water_mon_species, Monster.FEMALE)
    player_trainer = Player_Trainer("Lauryn", game, [fire_mon, grass_mon_2])
    ai_trainer = AI_Trainer("Computy", game, [water_mon]) 
    wild_trainer = Wild_Trainer([grass_mon])

    return player_trainer, ai_trainer, wild_trainer
    
    
if __name__=="__main__":
    import sys
    from Monster_ASCII_Game.game import MonsterGame
    display = MonsterGameDisplay()
    player = MonsterGamePlayer("Ash")
    game = MonsterGame(display, player)

    grass_mon_species, fire_mon_species, water_mon_species = create_monster_species() 
    #print("Created Species")
    #print("Grass:{}\nFire:{}\nWater:{}".format(grass_mon_species, fire_mon_species, water_mon_species))
   # print("----------------")
   # print(fire_mon_species.move_progression)
    grass_mon = Monster(grass_mon_species, Monster.FEMALE)
    grass_mon_2 = Monster(grass_mon_species, Monster.MALE)
    fire_mon = Monster(fire_mon_species, Monster.MALE)
    water_mon = Monster(water_mon_species, Monster.FEMALE)
    
   # print("Monsters\n{}\n{}\n{}\n{}".format(grass_mon, grass_mon_2, fire_mon, water_mon))
    player_trainer = Player_Trainer("Lauryn", game, [fire_mon, grass_mon_2])
    ai_trainer = AI_Trainer("Computy", game, [water_mon]) 
    wild_trainer = Wild_Trainer([grass_mon])
   # print("Trainers\n{}\n{}\n{}".format(player_trainer, ai_trainer, wild_trainer))
    game.new_battle(player_trainer, ai_trainer) 
