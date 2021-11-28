import sounddevice as sd
import scipy.io.wavfile as siw
import nxbt
import argparse
import macros
import time

FREQ = 44100      # Default sampling frequency
DELTA = 0.18      # Delta for element equality
REC_DURATION = 5  # Game sound recording duration [s]


def crop_sound_array(sound_array, freq, start_time, end_time):
    start_idx = int(freq * start_time)
    end_idx = int(freq * end_time)
    return sound_array[start_idx:end_idx]


def init_shiny_template():
    # Shiny stars sound template
    shiny_stars_file = "template_sounds/shiny_stars_recording.wav"
    freq, shiny_stars_array = siw.read(shiny_stars_file)
    # Crop start of the shiny stars recording
    start_time = 0.155  # Start time [s] to crop to
    end_time = 0.4     # End time [s] to crop to
    shiny_stars_array = crop_sound_array(shiny_stars_array, freq, start_time, end_time)
    return freq, shiny_stars_array


def record_game_sound(freq, duration):
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=1)
    sd.wait()
    return recording


def equals_with_delta(a, b, delta):
    return abs(abs(a) - abs(b)) < delta


def contains_subarray(array, subarray, delta):
    for i in range(len(array)):
        if equals_with_delta(subarray[0], array[i], delta):
            i += 1
            j = 1
            while i < len(array) and j < len(subarray) \
                    and equals_with_delta(subarray[j], array[i], delta):
                i += 1
                j += 1
            if j == len(subarray):
                return True
    return False


def record_and_check_shiny(freq, shiny_template_array, recording_duration):
    # Record game sound
    print("Recording game sound...")
    recording_array = record_game_sound(freq, recording_duration)
    # Check if recording includes shiny stars
    print("Checking presence of shiny...")
    return contains_subarray(recording_array, shiny_template_array, DELTA)


def synchronize_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER)
    print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
    nx.wait_for_connection(controller)
    print("Pro controller connected !")
    return controller


def reconnect_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER,
                                      reconnect_address=nx.get_switch_addresses())
    time.sleep(4)
    print("Pro controller connected !")
    return controller


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser()
    help = "Use this flag to bypass virtual controller synchronization, " \
           "and directly connect it to the console, " \
           "if this is not the first time you connect to a Switch."
    parser.add_argument("-r", "--reconnect", help=help, action="store_true")
    args = parser.parse_args()

    # Initialize template shiny sparkles array
    freq, shiny_template_array = init_shiny_template()

    # Initialize and connect virtual game controller, then go back to game
    nx = nxbt.Nxbt()
    if args.reconnect:
        controller = reconnect_controller(nx)
    else:
        controller = synchronize_controller(nx)
        nx.macro(controller, macros.GO_BACK_TO_GAME_AFTER_SYNC)

    '''
    # Record game sound, and check if shiny sparkles are present
    is_shiny = record_and_check_shiny(freq, shiny_template_array, REC_DURATION)
    print(is_shiny)
    '''
