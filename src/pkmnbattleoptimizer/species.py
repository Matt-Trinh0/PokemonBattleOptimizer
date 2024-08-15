from stats import BaseStat


class Species:
    def __init__(
        self,
        name: str = "",
        hp: int = 1,
        attack: int = 1,
        defense: int = 1,
        special_attack: int = 1,
        special_defense: int = 1,
        speed: int = 1,
        ability_1: str = "",
        ability_2: str = "",
        forms: list = None,
        type_1: str = "",
        type_2: str = "",
    ):
        self.name = name
        self.hp = BaseStat(hp)
        self.attack = BaseStat(attack)
        self.defense = BaseStat(defense)
        self.special_attack = BaseStat(special_attack)
        self.special_defense = BaseStat(special_defense)
        self.speed = BaseStat(speed)
        self.ability_1 = ability_1
        self.ability_2 = ability_2
        self.forms = forms
        self.type_1 = type_1
        self.type_2 = type_2
