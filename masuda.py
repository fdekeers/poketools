"""
Automates egg hatching for shiny hunting with Masuda method.
"""

import argparse
from utils.controller import Controller


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    # Egg cycles
    help = "Number of egg cycles before hatching for this specific Pokémon species."
    parser.add_argument("-c", "--egg-cycles", type=int, help=help)
    # Hatching steps
    help = "Number of steps before hatching for this specific Pokémon species."
    parser.add_argument("-s", "--egg-steps", type=int, help=help)
    args = parser.parse_args()

    # Initialize and connect virtual game controller, then go back to game
    controller = Controller()
    controller.sync_and_go_back()
