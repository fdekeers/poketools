import scipy.io.wavfile as wavfile
import sounddevice as sd
from scipy import signal

# Configuration variable
START_TIME = 0.155  # Start time [s] to crop the template sound to
END_TIME = 0.6  # End time [s] to crop the template sound to
THRESHOLD = 30  # Correlation threshold


def record_game_sound(freq, duration):
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    # Flatten recording, because recording is an array of 1-element arrays
    recording = [item for sublist in recording for item in sublist]
    return recording


def crop_sound_array(sound_array, freq, start_time, end_time):
    start_idx = int(freq * start_time)
    end_idx = int(freq * end_time)
    return sound_array[start_idx:end_idx]


def crop_audio_file(filename, start_time, end_time):
    cropped_filename = f"{filename.split('.')[0]}_cropped.wav"
    freq, audio_array = wavfile.read(filename)
    audio_array = crop_sound_array(audio_array, freq, start_time, end_time)
    wavfile.write(cropped_filename, freq, end_time - start_time)


def contains_sound(template_file, full_array):
    # Open sound files
    freq, template_array = wavfile.read(template_file)
    # Apply correlation
    correlation = signal.correlate(template_array, full_array, mode="valid", method="fft")
    peak = max(max(correlation), abs(min(correlation)))
    # Audio template found if correlation peak is more than THRESHOLD times more than average value
    found = peak >= THRESHOLD
    return found, correlation


def record_and_save(freq, duration, filename):
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    wavfile.write(filename, freq, duration)
