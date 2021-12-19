import sounddevice as sd
import scipy.io.wavfile as wavfile
import librosa
from scipy import signal


# Configuration variable
START_TIME = 0.155  # Start time [s] to crop the template sound to
END_TIME = 0.6      # End time [s] to crop the template sound to
THRESHOLD = 20      # Correlation threshold


def record_game_sound(freq, duration, audio_file_name):
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=1)
    sd.wait()
    wavfile.write(audio_file_name, freq, recording)


def crop_sound_array(sound_array, freq, start_time, end_time):
    start_idx = int(freq * start_time)
    end_idx = int(freq * end_time)
    return sound_array[start_idx:end_idx]


def contains_sound(template_file, full_file):
    # Open sound files
    y_template, sample_rate = librosa.load(template_file, sr=None)
    y_full, _ = librosa.load(full_file, sr=sample_rate)
    # Apply correlation
    correlation = signal.correlate(y_template, y_full, mode="valid", method="fft")
    peak = max(correlation)
    # Audio template found if correlation peak is more than THRESHOLD times more than average value
    found = peak >= THRESHOLD
    return found, correlation
