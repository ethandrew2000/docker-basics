"""Generate a tabletop adventure party and print its ability scores."""

import argparse
import os
import random

from rich import box
from rich.console import Console
from rich.table import Table


NAMES = (
    "Mira Stormbrook", "Thorn Ashvale", "Rook Ironwood",
    "Lyra Moonfern", "Pip Quickstep", "Nora Emberfall",
)
ROLES = ("Warrior", "Wizard", "Ranger", "Bard", "Healer", "Rogue")
ABILITIES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")


def roll_ability(rng):
    """Roll four six-sided dice and discard the lowest die."""
    dice = [rng.randint(1, 6) for _ in range(4)]
    return sum(dice) - min(dice)


def generate_party(count, rng):
    if not 1 <= count <= len(NAMES):
        raise ValueError("Party size must be between 1 and 6")
    return [
        {
            "name": name,
            "role": rng.choice(ROLES),
            "scores": [roll_ability(rng) for _ in ABILITIES],
        }
        for name in rng.sample(NAMES, count)
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, choices=range(1, 7), default=3,
                        help="number of adventurers, from 1 to 6 (default: 3)")
    parser.add_argument("--seed", type=int, help="repeat a party using a fixed seed")
    args = parser.parse_args(argv)
    party = generate_party(args.count, random.Random(args.seed))
    app_env = os.getenv("APP_ENV", "development")

    print(f"Dungeon Party Generator | Environment: {app_env}")
    print("Ability scores: roll four six-sided dice and drop the lowest.")
    table = Table(title="Your Adventure Party", box=box.ASCII, highlight=False)
    table.add_column("Adventurer", style="cyan")
    table.add_column("Role", style="magenta")
    for ability in ABILITIES:
        table.add_column(ability, justify="right")
    for hero in party:
        table.add_row(hero["name"], hero["role"], *map(str, hero["scores"]))
    Console(markup=False).print(table)
    print(f"Your party of {len(party)} is ready to explore the dungeon!")


if __name__ == "__main__":
    main()
