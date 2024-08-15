from math import floor, prod
from enum import Enum

from nature import Nature


class BaseStatType(Enum):
    HP = 0
    ATTACK = 1
    DEFENSE = 2
    SPECIAL_ATTACK = 3
    SPECIAL_DEFENSE = 4
    SPEED = 5


class BaseStat:
    def __init__(self, value: int, stat_type: BaseStatType):
        self._value = value
        self._stat_type = stat_type

    @property
    def value(self):
        return self._value

    @property
    def stat_type(self):
        return self._stat_type

    @value.setter
    def value(self, value: int):
        if value < 0 or value > 255:
            raise ValueError(f"A base stat must be between 0 and 255. Got {value}")
        self._value = value


class IndividualValue:
    def __init__(self, value: int):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value < 0 or value > 31:
            raise ValueError(
                f"An individual value must be between 0 and 31. Got {value}"
            )


class EffortValue:
    def __init__(self, value: int):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value < 0 or value > 255:
            raise ValueError(f"An effort value must be between 0 and 255. Got {value}")


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

        if base_stat.stat_type == BaseStatType.HP:
            no_mod_stat = base_term + level + 10
        else:
            no_mod_stat = floor(
                (base_term + 5) * nature.get_modifier(base_stat.stat_type)
            )

        stage_multiplier = (
            self._stage / 2 if self._stage >= 0 else 2 / (abs(self._stage) + 2)
        )

        return prod([no_mod_stat, stage_multiplier] + modifiers)
