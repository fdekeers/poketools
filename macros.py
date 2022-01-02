"""
List of macros used by the virtual controller.
"""

GO_BACK_TO_GAME_AFTER_SYNC = """
2s
A 0.1s
1s
B 0.1s
1s
DPAD_UP 0.1s
0.5s
DPAD_LEFT 1s
A 0.1s
1s
"""

START_BATTLE = """
L_STICK@+000+100 0.3s
LOOP 10
    A 0.1s
    0.2s
"""

RESET_GAME = """
HOME 0.05s
0.5s
B 0.1s
0.1s
X 0.1s
0.2s
A 0.1s
0.3s
A 0.1s
LOOP 119
    A 0.1s
    0.2s
"""

SLEEP_MODE = """
HOME 2s
A 0.1s
"""

BUSY_WAIT = """
LOOP {}
    A 0.1s
    0.1s
"""