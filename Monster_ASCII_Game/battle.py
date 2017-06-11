from Monster_ASCII_Game.trainer import *
from Monster_ASCII_Game.monster import *

class Battle:
    DRAW = "Draw"
    NO_WINNER_YET = "No Winner Yet"
    def __init__(self, trainers):
        if(len(trainers)>=2):
            self.trainers = trainers
        else:
            raise ValueError("Battle requires at least 2 trainers")
        self.winner = self.NO_WINNER_YET
    def round(self):
        while(self.winner==self.NO_WINNER_YET):
            self.trainer_turns()
    def trainer_turns(self):
        for trainer in self.trainers:
            has_fainted = trainer.decide()
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
def create_types():
    water_type = Element_Type("Water") 
    fire_type = Element_Type("Fire") 
    grass_type = Element_Type("Grass")
    normal_type = Element_Type("Normal")
    #Weaknesses
    water_type.weaknesses=[grass_type]
    fire_type.weaknesses=[water_type]
    grass_type.weaknesses=[fire_type]
    #Resistences
    water_type.resistences = [fire_type]
    fire_type.resistences = [grass_type]
    grass_type.resistences = [water_type]
def create_player_trainer():
    
if __name__=="__main__":
    display = MonsterGameDisplay()
    player = MonsterGamePlayer("Ash")
    game = MonsterGame(display, player)
    player_trainer = Player_Trainer(name)
    trainers = []
    battle = Battle()
