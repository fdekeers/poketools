import sounddevice as sd
import scipy.io.wavfile as siw


if __name__ == "__main__":

    # Record game sound
    freq = 44100  # Sampling frequency [Hz]
    duration = 1  # Recording duration [s]
    recording = sd.rec(int(duration*freq), samplerate=freq, channels=1)
    sd.wait()

    # Save recording to file
    siw.write("template.wav", freq, recording)
