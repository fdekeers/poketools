import argparse


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    help = "Number of egg cycles before hatching for this specific Pokémon species."
    parser.add_argument("-c", "--egg-cycles", type=int, help=help)
    help = "Number of steps before hatching for this specific Pokémon species."
    parser.add_argument("-s", "--egg-steps", type=int, help=help)
    args = parser.parse_args()
