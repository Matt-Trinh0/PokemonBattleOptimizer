import os

from pokemon import Pokemon
from stats import StatType, IndividualValue, EffortValue
from nature import Nature
from pokemon_type import Type


class ShowdownConverter:
    def loads(self, pokemon: str):
        # TODO This
        line_split = pokemon.strip().split("\n")

        # Map of strings to detect for triggering parsing
        line_parse_map = {
            "species_and_item": {"check": "@", "func": self._parse_species_and_item},
            "level": {"check": "Level", "func": self._parse_level},
            "nature": {"check": "Nature", "func": self._parse_nature},
            "tera": {"check": "Tera", "func": self._parse_tera},
            "ability": {"check": "Ability", "func": self._parse_ability},
            "evs": {
                "check": "EVs",
                "func": lambda value: self._parse_stat_values(value, "ev"),
            },
            "ivs": {
                "check": "IVs",
                "func": lambda value: self._parse_stat_values(value, "iv"),
            },
            "moves": {"check": "- ", "func": self._parse_move},
        }

        pokemon_buffer = {}
        pokemon = []
        for line in line_split:
            # When there is a blank line, flush the buffer into a pokemon and go to next loop iteration
            if not line.strip():
                # TODO Create the pokemon from the buffer data
                pokemon.append(Pokemon())
                pokemon_buffer = {}
                continue

            line_parser = next(
                (key, parser["func"])
                for key, parser in line_parse_map.items()
                if parser["check"] in line
            )
            if line_parser:
                pokemon_buffer[line_parser[0]] = line_parser[1](line)

    def _parse_species_and_item(self, species_and_item: str):
        species, item = (token.strip() for token in species_and_item.split("@"))
        return species, item

    def _parse_level(self, level: str):
        return int(level[7:])

    def _parse_nature(self, nature: str):
        # TODO Fix this once nature look ups are implemented
        return Nature(nature[:-7])

    def _parse_tera(self, tera: str):
        return Type(tera[11:].strip().upper())

    def _parse_ability(self, ability: str):
        # TODO Implement once abilites are in
        return ability[9:]

    def _parse_move(self, move: str):
        # TODO Implement this properly once moves are implemented
        return move[2:]

    def _parse_stat_values(self, stat_values: str, mode: str):
        if mode not in ("ev", "iv"):
            raise ValueError(
                f"Invalid mode specified for parsing stat values. Got {mode}, expected 'iv' or 'ev'"
            )

        stats_str = stat_values[5:]
        # Abusing the index as the value for this "map"
        stat_map = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        values = {}
        for stat_str in stats_str.split("/"):
            value = stat_str.strip().split(" ")
            values[StatType(stat_map.index(value[1]))] = int(value[0])

        default_values = {"ev": 0, "iv": 31}
        default_stats = {
            StatType(i): default_values[mode]
            for i in range(len(stat_map))
            if StatType(i) not in values.keys()
        }
        values.update(default_stats)

        value_type = {"ev": EffortValue, "iv": IndividualValue}

        values = {stat: value_type(value, stat) for stat, value in values.items()}

        return values
