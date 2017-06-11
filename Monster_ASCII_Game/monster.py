import random
MAX_NUM_MOVES = 4
class Type_Difference:
    def __init__(self, element_type, multiplier):
        self.element_type = element_type
        self.multiplier = multiplier
    def __str__(self):
        return "Element Type:{}, Multipler:{}".format(self.element_type, self.multiplier)
    def __repr__(self):
        return self.element_type.__repr__()
class Element_Type:
    def __init__(self, name, weaknesses=[], resistences=[]):
        self.name = name
        self.weaknesses = weaknesses
        self.resistences = resistences
    def __str__(self):
        return "Name:{}, Weaknesses:{}, Resistences:{}".format(self.name, self.weaknesses, self.resistences)
    def __repr__(self):
        return self.name
class Move:
    HEALTH = "Health"
    ATTACK = "Attack"
    DEFENSE = "Defense"
    SPEED = "Speed"
    EFFECTS = [HEALTH, ATTACK, DEFENSE, SPEED] 
    def __init__(self, name, effect_type, element_type, max_value):
        self.name = name
        if(effect_type in Move.EFFECTS):
            self.effect_type = effect_type
        else:
            raise ValueError("move effect type not recognized")
        self.max_value = max_value
        self.element_type = element_type
        
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
class Species:
    def __init__(self, name, element_type, move_progression, health_progression, speed_progression, attack_progression, defense_progression, experience_multiplier):
        self.name = name
        self.element_type = element_type
        self.move_progression = move_progression
        self.health_progression = health_progression
        self.attack_progression = attack_progression
        self.speed_progression = speed_progression
        self.defense_progression = defense_progression
        self.experience_multiplier = experience_multiplier
    def calc_health(self, level):
        return self.health_progression[level]
    def calc_attack(self, level):
        return self.attack_progression[level]
    def calc_speed(self, level):
        return self.speed_progression[level]
    def calc_defense(self, level):
        return self.defense_progression[level]
    def init_moves(self, level):
        possible_moves = [move for min_level, move in self.move_progression.items() if min_level<=level]
        if(len(possible_moves)>MAX_NUM_MOVES):
            moves = []
            for _i in MAX_NUM_MOVES:
                move = random.choice(possible_moves)
                moves.append(move)
                possible_moves.remove(move)
            return moves
        else:
            return possible_moves

    def __str__(self):
        return "Name:{}, ElementType:{}".format(self.name, self.element_type)
    def __repr__(self):
        return self.name
class Monster:
        FEMALE = "female"
        MALE = "male"
        GENDER_NONE = "none"
        GENDERS = [FEMALE, MALE, GENDER_NONE]
        def __init__(self, species, gender, level=5, name=None):
            self.species = species
            if(gender in Monster.GENDERS):
                self.gender = gender
            else:
                raise ValueError("gender not recognized")
            if(not name):
                self.name = species.name
            else:
                self.name  = name
            self.level = level
            self.init_moves()
            self.init_stats()
            self.heal()
        def init_stats(self):
            self.max_health = self.species.calc_health(self.level)  
            self.max_attack = self.species.calc_attack(self.level)
            self.max_speed = self.species.calc_speed(self.level)
            self.max_defense = self.species.calc_defense(self.level)
        def init_moves(self):
            self.moves = self.species.init_moves(self.level)
        def attack_monster(self, target, move):
            if(move.effect_type == Move.HEALTH):
                target.health += move.max_value
            elif(move.effect_type == Move.SPEED):
                target.speed += move.max_value
            elif(move.effect_type == Move.ATTACK):
                target.attack += move.max_value
            elif(move.effect_type == Move.DEFENSE):
                target.defense += move.max_value
            else:
                raise ValueError("attack move type not recognized")

        def heal(self):
            self.health = self.max_health 
            self.attack = self.max_attack
            self.speed = self.max_speed
            self.defense = self.max_defense
        def __str__(self):
            return "Name:{}, Species:{}, Health:{}, Moves:{}".format(self.name, self.species, self.health, self.moves)
        def __repr__(self):
            return self.__str__()

