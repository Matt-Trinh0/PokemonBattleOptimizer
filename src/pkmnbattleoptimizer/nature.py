from stats import StatType


class Nature:
    def __init__(
        self, name: str, decrease_stat: StatType, increase_stat: StatType
    ):
        self.name = name
        self._decrease_stat = decrease_stat
        self._increase_stat = increase_stat

    def get_modifier(self, base_stat_type: StatType) -> float:
        if base_stat_type == self._decrease_stat:
            return 0.9
        elif base_stat_type == self._increase_stat:
            return 1.1
        else:
            return 1

    # TODO Need look up functionality based off of name for converters