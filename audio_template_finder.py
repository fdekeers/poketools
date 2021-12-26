import sounddevice as sd
import scipy.io.wavfile as wavfile
from scipy import signal


# Configuration variable
START_TIME = 0.155  # Start time [s] to crop the template sound to
END_TIME = 0.6      # End time [s] to crop the template sound to
THRESHOLD = 20      # Correlation threshold


def record_game_sound(freq, duration):
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=1)
    sd.wait()
    # Flatten recording, because recording is an array of 1-element arrays
    recording = [item for sublist in recording for item in sublist]
    return recording


def crop_sound_array(sound_array, freq, start_time, end_time):
    start_idx = int(freq * start_time)
    end_idx = int(freq * end_time)
    return sound_array[start_idx:end_idx]


def contains_sound(template_file, full_array):
    # Open sound files
    freq, template_array = wavfile.read(template_file)
    # Apply correlation
    correlation = signal.correlate(template_array, full_array, mode="valid", method="fft")
    peak = max(max(correlation), abs(min(correlation)))
    # Audio template found if correlation peak is more than THRESHOLD times more than average value
    found = peak >= THRESHOLD
    return found, correlation
