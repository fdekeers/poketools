import sounddevice as sd
import scipy.io.wavfile as siw
import nxbt

FREQ = 44100   # Default sampling frequency
DELTA = 0.18   # Delta for element equality


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


if __name__ == "__main__":

    # Initialize template shiny array
    freq, shiny_template_array = init_shiny_template()

    # Record game sound
    duration = 5  # Recording duration [s]
    print("Recording game sound...")
    recording_array = record_game_sound(freq, duration)

    # Check if recording includes shiny stars
    print("Checking presence of shiny...")
    isShiny = contains_subarray(recording_array, shiny_template_array, DELTA)
    print(isShiny)

