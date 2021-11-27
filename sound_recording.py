import sounddevice as sd
import scipy.io.wavfile as siw


def record_game_sound(freq, duration):
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=1)
    sd.wait()
    return recording


def contains_subarray(array, pattern):
    for i in range(len(array)):
        if pattern[0] == array[i]:
            i += 1
            j = 1
            while i < len(array) and j < len(pattern) and pattern[j] == array[i]:
                i += 1
                j += 1
            if j == len(pattern):
                return True
    return False


if __name__ == "__main__":

    # Shiny stars sound template
    shiny_stars_file = "shiny_stars_recording.wav"
    freq, shiny_stars_array = siw.read(shiny_stars_file)


    '''
    # Record game sound
    duration = 5  # Recording duration [s]
    recording_array = record_game_sound(freq, duration)
    '''

    f, game_recording = siw.read("game_recording_2.wav")
    game_recording = game_recording.tolist()
    result = contains_subarray(game_recording, shiny_stars_array)
