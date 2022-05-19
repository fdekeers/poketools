"""
Audio utilities to record and compare audio files.
"""

import os
import stat
import scipy.io.wavfile as wavfile
import sounddevice as sd
from scipy import signal
import matplotlib.pyplot as plt

# Configuration variable
FREQ = 44100        # Default sampling frequency
START_TIME = 0.155  # Start time [s] to crop the template sound to
END_TIME = 0.6      # End time [s] to crop the template sound to
THRESHOLD = 30      # Correlation threshold


def record_game_sound(duration):
    """
    record the sound from the game
    @param duration: time for the recording, in seconds
    """
    recording = sd.rec(int(duration * FREQ), samplerate=FREQ, channels=1)
    sd.wait()
    # Flatten recording, because recording is an array of 1-element arrays
    recording = [item for sublist in recording for item in sublist]
    return recording


def crop_sound_array(sound_array, start_time, end_time):
    """
    slice the values of the sound array from start_time until end_time
    @param sound_array: sound to extract
    @param start_time: start of the slice to return
    @param end_time: end of the slice to return
    @return: slice of the signal between start_time and until end_time
    """
    return sound_array[int(FREQ * start_time):int(FREQ * end_time)]


def crop_audio_file(filename, start_time, end_time):
    """
    rewrite an audio file, to give its values from start_time until end_time
    @param filename: file where the audio is written
    @param start_time: start of the slice to return
    @param end_time: end of the slice to return
    @return: None. Rewrite the content of the audio file to extract its values in [start_time:end_time]
    """
    cropped_filename = f"{filename.split('.')[0]}_cropped.wav"
    freq, audio_array = wavfile.read(filename)
    audio_array = crop_sound_array(audio_array, start_time, end_time)
    wavfile.write(cropped_filename, freq, end_time - start_time)


def contains_sound(template_file, full_array):
    """
    tell if the sound contained within an array matches a template sound
    @param template_file: file where the expected sound to find is written
    @param full_array: sound to compare
    @return: found, correlation
        - found: bool value set to True if the 2 sounds match
        - correlation: correlation between the 2 sounds
    """
    # Open sound files
    freq, template_array = wavfile.read(template_file)
    # Apply correlation
    correlation = signal.correlate(template_array, full_array, mode="valid", method="fft")
    peak = max(max(correlation), abs(min(correlation)))
    # Audio template found if correlation peak is more than THRESHOLD times more than average value
    found = peak >= THRESHOLD
    return found, correlation


def record_and_save(duration, filename):
    """
    record the sound from the game and save it into a file
    @param duration: duration of the recording
    @param filename: file where to write the recording
    @return: None. Save the recording
    """
    recording = sd.rec(int(duration * FREQ), samplerate=FREQ, channels=1)
    sd.wait()
    wavfile.write(filename, FREQ, duration)


def save_plot(correlation, plot_file):
    """
    save a plot of the correlation between the recorded game sound and the expected shiny sound to find
    @param correlation: correlation between 2 signals
    @param plot_file: file to save the plot to
    @return: None. Save a plot of the correlation into correlation.png
    """
    fig, ax = plt.subplots()
    ax.plot(correlation)
    fig.savefig(plot_file)
    permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH
    os.chmod(plot_file, permission)
    plt.close(fig)


def record_and_check_shiny(shiny_template_file, recording_duration):
    """
    record the sound from the game and tell if it is a shiny sound
    @param shiny_template_file: file where the sound for shiny pokemon is written
    @param recording_duration: duration for the recording
    @return: True if the sound from the game contained a shiny pokemon
    """
    # Record game sound
    print("Recording game sound...")
    game_recording = record_game_sound(recording_duration)
    # Check if recording includes shiny sparkles
    print("Checking presence of shiny...")
    return contains_sound(shiny_template_file, game_recording)


def assign_device(devicename):
    try:
        sd.check_input_settings(device=devicename)
        sd.default.device = devicename
    except:
        print("Device settings not supported")
        exit()
