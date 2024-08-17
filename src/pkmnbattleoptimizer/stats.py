from math import floor, prod
from enum import Enum

from nature import Nature


class StatType(Enum):
    HP = 0
    ATTACK = 1
    DEFENSE = 2
    SPECIAL_ATTACK = 3
    SPECIAL_DEFENSE = 4
    SPEED = 5


class Stat:
    def __init__(
        self,
        value: int,
        min_value: int,
        max_value: int,
        stat_type: StatType,
        name: str = "stat",
    ):
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._state_type = stat_type
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value < self._min_value or value > self._max_value:
            raise ValueError(
                f"A {self._name} must be between {self._min_value} and {self._max_value}. Got {value}"
            )
        self._value = value

    @property
    def stat_type(self):
        return self._stat_type


class BaseStat(Stat):
    def __init__(self, value: int, stat_type: StatType):
        super().__init__(value, 0, 255, stat_type, "base stat")


class IndividualValue(Stat):
    def __init__(self, value: int, stat_type: StatType):
        super().__init__(value, 0, 31, stat_type, "individual value")


class EffortValue(Stat):
    def __init__(self, value: int, stat_type: StatType):
        super().__init__(value, 0, 255, stat_type, "effort value")


class EffectiveStat:
    def __init__(self):
        self._stage = 0
        self._value = 0

    @property
    def stage(self):
        return self._stage

    @property
    def value(self):
        return self._value

    @stage.setter
    def stage(self, value: int):
        if value < -6 or value > 6:
            raise ValueError(f"Stat stage must be between -6 and -6. Got {value}")
        self._stage = value

    def calculate_value(
        self,
        base_stat: BaseStat,
        individual_value: IndividualValue,
        effort_value: EffortValue,
        nature: Nature,
        level: int,
        modifiers: list[float],
    ) -> value:
        # https://bulbapedia.bulbagarden.net/wiki/Stat#Generation_III_onward
        base_term = floor(
            (2 * base_stat.value + individual_value + floor(effort_value / 4) * level)
            / 100
        )

        if base_stat.stat_type == StatType.HP:
            no_mod_stat = base_term + level + 10
        else:
            no_mod_stat = floor(
                (base_term + 5) * nature.get_modifier(base_stat.stat_type)
            )

        stage_multiplier = (
            self._stage / 2 if self._stage >= 0 else 2 / (abs(self._stage) + 2)
        )

        return prod([no_mod_stat, stage_multiplier] + modifiers)
