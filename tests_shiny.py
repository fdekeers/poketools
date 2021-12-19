import unittest
import matplotlib.pyplot as plt
import audio_template_finder as atf
from pathlib import Path


TEMPLATE_FILE   = "template_sounds/shiny/template_cropped.wav"
CORRELATION_DIR = "correlations"


def run_test(file_to_test, correlation_file):
    Path(CORRELATION_DIR).mkdir(parents=True, exist_ok=True)
    actual, correlation = atf.contains_sound(TEMPLATE_FILE, file_to_test)
    fig, ax = plt.subplots()
    ax.plot(correlation)
    fig.savefig(correlation_file)
    return actual


class TestBase(unittest.TestCase):
    def test_base(self):
        file_to_test = "template_sounds/shiny/test/base.wav"
        correlation_file = f"{CORRELATION_DIR}/correlation_base.png"
        self.assertFalse(run_test(file_to_test, correlation_file))


class TestPokeball(unittest.TestCase):
    def test_pokeball(self):
        file_to_test = "template_sounds/shiny/test/pokeball.wav"
        correlation_file = f"{CORRELATION_DIR}/correlation_pokeball.png"
        self.assertFalse(run_test(file_to_test, correlation_file))


class TestIntimidate(unittest.TestCase):
    def test_intimidate(self):
        file_to_test = "template_sounds/shiny/test/intimidate.wav"
        correlation_file = f"{CORRELATION_DIR}/correlation_intimidate.png"
        self.assertFalse(run_test(file_to_test, correlation_file))


class TestShiny(unittest.TestCase):
    def test_shiny(self):
        file_to_test = "template_sounds/shiny/test/shiny.wav"
        correlation_file = f"{CORRELATION_DIR}/correlation_shiny.png"
        self.assertTrue(run_test(file_to_test, correlation_file))


if __name__ == '__main__':
    unittest.main()
