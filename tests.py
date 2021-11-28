import unittest
import scipy.io.wavfile as siw
import shiny_reset as sr


def run_test_with_file(game_recording_file):
    _, recording_array = siw.read(game_recording_file)
    _, shiny_template_array = sr.init_shiny_template()
    actual = sr.contains_subarray(recording_array, shiny_template_array, sr.DELTA)
    return actual


class TestBase(unittest.TestCase):
    def test_base(self):
        self.assertFalse(run_test_with_file("template_sounds/game_recording_base.wav"))


class TestPokeball(unittest.TestCase):
    def test_pokeball(self):
        self.assertFalse(run_test_with_file("template_sounds/game_recording_pokeball.wav"))


class TestIntimidate(unittest.TestCase):
    def test_intimidate(self):
        self.assertFalse(run_test_with_file("template_sounds/game_recording_intimidate.wav"))


class TestShiny(unittest.TestCase):
    def test_shiny(self):
        self.assertTrue(run_test_with_file("template_sounds/game_recording_shiny.wav"))


if __name__ == '__main__':
    unittest.main()
