import os
import stat
import audio_template_finder as atf
import matplotlib.pyplot as plt
import nxbt
import argparse
import macros
import time
import dbus


# Configuration variables
FREQ = 44100       # Default sampling frequency
DELTA = 0.18       # Delta for element equality
REC_DURATION = 3   # Game sound recording duration [s]
SAVE_PLOT = False  # Save correlation plot

# Template audio file
SHINY_AUDIO_FILE = "template_sounds/shiny/template_cropped.wav"

# Number of resets
number_of_resets = 0


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
    game_recording = atf.record_game_sound(freq, recording_duration)
    # Check if recording includes shiny sparkles
    print("Checking presence of shiny...")
    is_shiny, correlation = atf.contains_sound(shiny_template_file, game_recording)
    # Plot correlation if required
    if SAVE_PLOT:
        save_plot(correlation)
    return is_shiny


def proceed_shiny(is_shiny, controller):
    global number_of_resets
    if is_shiny:
        print(f"Shiny found after {number_of_resets} resets.")
        # Shiny ! Put console in sleep mode
        nx.macro(controller, macros.SLEEP_MODE)
        exit(0)
    else:
        # Not shiny, reset game
        number_of_resets += 1
        print(f"No shiny found. Reset n°{number_of_resets}.")
        nx.macro(controller, macros.RESET_GAME)


def synchronize_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER)
    print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
    nx.wait_for_connection(controller)
    print("Pro controller connected !")
    return controller


def reconnect_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER,
                                      reconnect_address=nx.get_switch_addresses())
    time.sleep(5)
    return controller


def busy_wait(controller, seconds):
    iterations = seconds * 5
    nx.macro(controller, macros.BUSY_WAIT.format(iterations))


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
        # Main loop in a try...except block to restart in case of crash
        try:
            # Initiate battle with Pokemon
            nx.macro(controller, macros.START_BATTLE)
            # Wait for the shiny sparkles to appear,
            # while using the controller to prevent it from disconnecting
            seconds = 9  # Change this depending on your battle loading time
            busy_wait(controller, seconds)
            # Record game sound, and check if shiny sparkles are present
            is_shiny = record_and_check_shiny(FREQ, SHINY_AUDIO_FILE, REC_DURATION)
            proceed_shiny(is_shiny, controller)
        except dbus.exceptions.DBusException:  # A problem occurred, try to recover
            is_shiny = record_and_check_shiny(FREQ, SHINY_AUDIO_FILE, 10)
            print("Controller crashed, reconnecting...")
            controller = reconnect_controller(nx)
            proceed_shiny(is_shiny, controller)
