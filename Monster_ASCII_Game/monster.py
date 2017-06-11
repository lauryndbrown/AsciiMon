import random
MAX_NUM_MOVES = 4
class Type_Difference:
    def __init__(self, element_type, multiplier):
        self.element_type = element_type
        self.multiplier = multiplier
class Element_Type:
    def __init__(self, name, weaknesses=[], resistences=[]):
        self.name = name
        self.weaknesses = weaknesses
        self.resistences = resistences
class Move:
    HEALTH = "Health"
    ATTACK = "Attack"
    DEFENSE = "Defense"
    SPEED = "Speed"
    EFFECTS = [EFFECT_DAMAGE, EFFECT_STATUS_ATTACK,EFFECT_STATUS_DEFENSE, EFFECT_STATUS_SPEED] 
    def __init__(self, name, effect_type, max_value):
        self.name = name
        if(effect_type in Move.EFFECTS):
            self.effect_type = effect_type
        else:
            raise ValueError("move effect type not recognized")
        self.max_value = max_value
        
class Species:
    def __init__(self, name, species_type, moves, health_progression, speed_progression, attack_progression, defense_progression, experience_multiplier):
        self.name = name
        self.species_type = species_type
        self.moves = moves
        self.health_progression = health_progression
        self.attack_progression = attack_progression
        self.speed_progression = speed_progression
        self.defense_progression = defense_progression
        self.experience_multipler = experience_multipler
    def calc_health(self, level):
        return self.health_progression[level]
    def init_moves(self, level):
        possible_moves = [move for min_level, move in self.moves if min_level<=self.level]
        if(possible_moves>MAX_NUM_MOVES):
            moves = []
            for _i in MAX_NUM_MOVES:
                move = random.choice(possible_moves)
                moves.append(move)
                possible_moves.remove(move)
            return moves
        else:
            return possible_moves
class Monster:
        GENDER_FEMALE = "female"
        GENDER_MALE = "male"
        GENDER_NONE = "none"
        GENDERS = [GENDER_FEMALE, GENDER_MALE, GENDER_NONE]
        def __init__(self, species, gender, moves, level=5, name=None):
            self.species = species
            if(gender in Monster.GENDERS):
                self.gender = gender
            else:
                raise ValueError("gender not recognized")
            if(not name):
                self.name = species
            else:
                self.name  = name
            self.level = level
            self.moves = moves
            self.init_stats()
            self.heal()
        def init_stats(self):
            self.max_health = species.calc_health(self.level)  
            self.max_attack = species.calc_attack(self.level)
            self.max_speed = species.calc_speed(self.level)
            self.max_defense = species.calc_level(self.level)
        def attack(self, target, move):
            if(move.effect_type == Move.HEALTH):
                target.health += move.max_value
            else if(move.effect_type == Move.SPEED):
                target.speed += move.max_value
            else if(move.effect_type == Move.ATTACK):
                target.attack += move.max_value
            else if(move.effect_type == Move.DEFENSE):
                target.defense += move.max_value
            else:
                raise ValueError("attack move type not recognized")

        def heal(self):
            self.health = self.max_health 
            self.attack = self.max_attack
            self.speed = self.max_speed
            self.defense = self.max_defense

