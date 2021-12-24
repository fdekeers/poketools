import os
import stat
import audio_template_finder as atf
import matplotlib.pyplot as plt
import nxbt
import argparse
import macros
import time


# Configuration variables
FREQ = 44100       # Default sampling frequency
DELTA = 0.18       # Delta for element equality
REC_DURATION = 5   # Game sound recording duration [s]
SAVE_PLOT = False  # Save correlation plot

# Audio files
GAME_RECORDING_FILE = ".game_recording.wav"
SHINY_AUDIO_FILE = "template_sounds/shiny/template_cropped.wav"


def save_plot(correlation):
    fig, ax = plt.subplots()
    ax.plot(correlation)
    plot_file = "correlation.png"
    fig.savefig(plot_file)
    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH
    os.chmod(plot_file, permission)


def record_and_check_shiny(freq, shiny_template_file, recording_duration):
    # Record game sound
    print("Recording game sound...")
    atf.record_game_sound(freq, recording_duration, GAME_RECORDING_FILE)
    # Check if recording includes shiny sparkles
    print("Checking presence of shiny...")
    is_shiny, correlation = atf.contains_sound(shiny_template_file, GAME_RECORDING_FILE)
    # Plot correlation if required
    if SAVE_PLOT:
        save_plot(correlation)
    # Delete game recording audio file
    os.remove(GAME_RECORDING_FILE)
    return is_shiny


def synchronize_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER)
    print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
    nx.wait_for_connection(controller)
    print("Pro controller connected !")
    return controller


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    help = "Use this flag to save a plot of the correlation between the recorded audio " \
           "and the shiny sparkles audio template."
    parser.add_argument("-p", "--plot-correlation", help=help, action="store_true")
    args = parser.parse_args()
    SAVE_PLOT = args.plot_correlation

    # Initialize and connect virtual game controller, then go back to game
    nx = nxbt.Nxbt()
    controller = synchronize_controller(nx)
    nx.macro(controller, macros.GO_BACK_TO_GAME_AFTER_SYNC)

    is_shiny = False
    while not is_shiny:
        # Initiate battle with Pokemon
        #nx.macro(controller, macros.START_BATTLE)

        # Record game sound, and check if shiny sparkles are present
        time.sleep(10)
        is_shiny, _ = record_and_check_shiny(FREQ, SHINY_AUDIO_FILE, REC_DURATION)
        if is_shiny:
            print("SHINY DETECTED ! Just catch it !")
            # Shiny ! Put console in sleep mode
            nx.macro(controller, macros.SLEEP_MODE)
        else:
            # Not shiny, reset game
            nx.macro(controller, macros.RESET_GAME)
