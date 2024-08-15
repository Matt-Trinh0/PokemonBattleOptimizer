from stats import BaseStatType


class Nature:
    def __init__(
        self, name: str, decrease_stat: BaseStatType, increase_stat: BaseStatType
    ):
        self.name = name
        self._decrease_stat = decrease_stat
        self._increase_stat = increase_stat

    def get_modifier(self, base_stat_type: BaseStatType) -> float:
        if base_stat_type == self._decrease_stat:
            return 0.9
        elif base_stat_type == self._increase_stat:
            return 1.1
        else:
            return 1
