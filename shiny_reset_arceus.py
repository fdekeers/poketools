# handle shiny resets
import os
import stat
import audio
import matplotlib.pyplot as plt
import nxbt
import argparse
import macros
import time
import threading


# Configuration variables
FREQ = 44100                # Default sampling frequency
REC_DURATION = 4            # Game sound recording duration [s]
GAME_LOADING_TIME = 36      # Game loading time [s] (Longer than the original script)
BATTLE_LOADING_TIME = 23    # Battle loading time [s] (Longer than the original script)
SAVE_PLOT = False           # Save correlation plot

# Template audio file
script_directory = os.path.dirname(os.path.abspath(__file__))  # current directory
SHINY_AUDIO_FILE = f"{script_directory}/template_sounds/shiny/template_cropped.wav"  # expected shiny sound to find

# Number of resets
number_of_resets = 0        # current resets done


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


def synchronize_controller(nx):
    """
    connect the controller for the first time
    wait for the user to allow the controller to connect, through the menu
    @param nx: nxbt instance
    @return: connected controller
    """
    controller = nx.create_controller(nxbt.PRO_CONTROLLER)
    print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
    nx.wait_for_connection(controller)
    print("Pro controller connected !")
    return controller


def reconnect_controller(nx):
    """
    reconnect the controller if it was not detected anymore
    wait for several seconds as the creation of a controller takes some time
    @param nx: nxbt instance
    @return: reconnected controller
    """
    controller = nx.create_controller(nxbt.PRO_CONTROLLER, reconnect_address=nx.get_switch_addresses())
    time.sleep(5)
    return controller


def busy_wait(controller, seconds):
    """
    press several time on the A key to ensure that the controller does not get disconnected
    @param controller: controller connected to the switch
    @param seconds: duration of the busy wait, in seconds
    @return: None. Press A key several time
    """
    busy_wait_macro(controller, macros.BUSY_WAIT.format(int(seconds * 5)))


def busy_wait_b(controller, seconds):
    """
    press several time on the N key to ensure that the controller does not get disconnected
    @param controller: controller connected to the switch
    @param seconds: duration of the busy wait, in seconds
    @return: None. Press B key several time
    """
    busy_wait_macro(controller, macros.BUSY_WAIT_B.format(int(seconds * 5)))


def busy_wait_macro(controller, macro):
    """
    send a macro to the controller using busy_wait
    @param controller: controller connected to the switch
    @param macro: macro sent to the controller
    @return: None. Execute the macro
    """
    nx.macro(controller, macro)


def busy_wait_background(controller, seconds):
    """
    starts a thread doing a busy wait operation
    @param controller:
    @param seconds:
    @return:
    """
    thread = threading.Thread(target=busy_wait, args=(controller, seconds))
    thread.start()


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    help = "Use this flag to save a plot of the correlation between the recorded audio " \
           "and the shiny sparkles audio template."
    parser.add_argument("-p", "--plot-correlation", help=help, action="store_true")
    args = parser.parse_args()
    SAVE_PLOT = args.plot_correlation

    # Initialize and connect virtual game controller, then go back to game
    print("Initializing...")
    nx = nxbt.Nxbt()
    time.sleep(5)  # Add delay for the Raspberry Pi
    controller = synchronize_controller(nx)
    nx.macro(controller, macros.GO_BACK_TO_GAME_AFTER_SYNC)

    is_shiny = False
    while not is_shiny:
        # Initiate battle with Pokemon
        print(f"Initiating a battle.")
        nx.macro(controller, macros.START_BATTLE_ARCEUS)
        # Wait for the shiny sparkles to appear,
        # while using the controller to prevent it from disconnecting
        busy_wait_b(controller, BATTLE_LOADING_TIME)
        # Record game sound, and check if shiny sparkles are present
        busy_wait_background(controller, REC_DURATION)
        is_shiny = record_and_check_shiny(FREQ, SHINY_AUDIO_FILE, REC_DURATION)
        if is_shiny:
            print(f"Shiny found after {number_of_resets} resets.")
            # Shiny ! Put console in sleep mode
            nx.macro(controller, macros.VIDEO)
            busy_wait_b(controller, 8)
            nx.macro(controller, macros.SLEEP_MODE)
            exit(0)
        else:
            # Not shiny, reset game
            number_of_resets += 1
            print(f"No shiny found. Reset n°{number_of_resets}.")
            # busy_wait_b(controller, 4)
            # nx.macro(controller, macros.RUN_FROM_BATTLE)
            # busy_wait(controller, 4.5)
            # nx.macro(controller, macros.RELOAD_MAP)
            nx.macro(controller, macors.RESET_GAME)
            busy_wait(controller, GAME_LOADING_TIME)
