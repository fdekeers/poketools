"""
Automates resets for shiny hunting stationary Pokémon.
"""

import os
import stat
from utils import audio
from utils.controller import Controller
import matplotlib.pyplot as plt
import argparse
from configs import general
import time
import threading


# Configuration variables
FREQ = 44100                                # Default sampling frequency
REC_DURATION = 4                            # Game sound recording duration [s]
SAVE_PLOT = False                           # Save correlation plot

# Template audio file
script_directory = os.path.dirname(os.path.abspath(__file__))  # current directory
SHINY_AUDIO_FILE = f"{script_directory}/template_sounds/shiny/template_cropped.wav"  # expected shiny sound to find

# Number of resets
number_of_resets = 0


def save_plot(correlation):
    """
    save a plot of the correlation between the recorded game sound and the expected shiny sound to find
    @param correlation: correlation between 2 signals
    @return: None. Save a plot of the correlation into correlation.png
    """
    fig, ax = plt.subplots()
    ax.plot(correlation)
    plot_file = f"{script_directory}/correlation.png"
    fig.savefig(plot_file)
    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH
    os.chmod(plot_file, permission)
    plt.close(fig)


def record_and_check_shiny(freq, shiny_template_file, recording_duration):
    """
    record the sound from the game and tell if it is a shiny sound
    @param freq: frequency for the recording
    @param shiny_template_file: file where the sound for shiny pokemon is written
    @param recording_duration: duration for the recording
    @return: True if the sound from the game contained a shiny pokemon
    """
    # Record game sound
    print("Recording game sound...")
    game_recording = audio.record_game_sound(freq, recording_duration)
    # Check if recording includes shiny sparkles
    print("Checking presence of shiny...")
    is_shiny, correlation = audio.contains_sound(shiny_template_file, game_recording)
    # Plot correlation if required
    if is_shiny and SAVE_PLOT:
        save_plot(correlation)
    return is_shiny


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    # Scenario (Pokemon we are trying to catch)
    possible_scenarios = [filename.split(".")[0][4:] for filename in os.listdir("configs") if filename[0:4] == "cfg_"]
    help = "Use this flag to specify what scenario the macros and timings should be set for." \
           "If the scenario you need is implemented, please contribute by adding it to the `configs` directory."
    parser.add_argument("-s", "--scenario", help=help, choices=possible_scenarios, default="ramanas")
    # Capture screenshot or video when shiny is found
    help = "Capture a video or screenshot once a shiny is found."
    parser.add_argument("-c", "--capture", help=help, choices=["video", "screenshot"])
    # Support for consoles with multiple users
    help = "Indicate the number of the user (1-8) that should be used to start the game, " \
           "or 0 if there is only one user that is selected automatically."
    parser.add_argument("-u", "--user", help=help, choices=list(range(0, 9)), default=0)
    # Plot correlation
    help = "Use this flag to save a plot of the correlation between the recorded audio " \
           "and the shiny sparkles audio template."
    parser.add_argument("-p", "--plot-correlation", help=help, action="store_true")
    help = "Select an audio input device by its name. Audio devices can be listed with `python3 -m sounddevice`."
    parser.add_argument("-d", "--device", help=help)
    args = parser.parse_args()
    config = getattr(__import__("configs", fromlist=[f"cfg_{args.scenario}"]), f"cfg_{args.scenario}")
    SAVE_PLOT = args.plot_correlation

    # Force no user switch for Shaymin scenario
    if args.scenario == "shaymin":
        args.user = 0

    # Confirm audio device exists
    if args.device:
        audio.assign_device(args.device)

    # Initialize and connect virtual game controller, then go back to game
    controller = Controller()
    controller.sync_and_go_back()

    is_shiny = False
    while not is_shiny:
        # Initiate battle with Pokemon
        print(f"Initiating a battle.")
        controller.macro(config.START_BATTLE)
        # Wait for the shiny sparkles to appear,
        # while using the controller to prevent it from disconnecting
        controller.busy_wait(config.BATTLE_LOADING_TIME)
        # Record game sound, and check if shiny sparkles are present
        controller.busy_wait_background(REC_DURATION)
        is_shiny = record_and_check_shiny(FREQ, SHINY_AUDIO_FILE, REC_DURATION)
        if is_shiny:
            print(f"Shiny found after {number_of_resets} resets.")
            # Shiny ! Put console in sleep mode
            if args.capture == "video": 
                controller.macro(general.VIDEO)
                controller.busy_wait_b(8)
            elif args.capture == "screenshot":
                controller.macro(general.SCREENSHOT)
            controller.macro(general.SLEEP_MODE)
            exit(0)
        else:
            # Not shiny, reset game
            number_of_resets += 1
            print(f"No shiny found. Reset n°{number_of_resets}.")
            controller.reset(config.RESET_GAME, int(args.user))
            controller.busy_wait(config.GAME_LOADING_TIME)
