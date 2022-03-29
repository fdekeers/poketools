# List of macros used by the virtual controller.

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

##########################
# MACROS FOR SHINY RESET #
##########################

START_BATTLE = """
A 0.1s
"""

RESET_GAME = """
HOME 0.05s
0.5s
B 0.1s
0.2s
X 0.1s
0.2s
A 0.1s
0.3s
A 0.1s
"""

RELOAD_MAP = """
L_STICK@+000-100 3.1s
0.1s
L_STICK@+000+100 3.1s
"""

RUN_FROM_BATTLE = """
LOOP 3
    DPAD_DOWN 0.1s
    0.1s
A 0.1s
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

BUSY_WAIT_B = """
LOOP {}
    B 0.1s
    0.1s
"""


#######################
# MACROS FOR EXP FARM #
#######################

STEPS_RECHARGE = """
L_STICK@+000+100 0.1s
L_STICK@-100-000 0.1s
L_STICK@+000-100 0.1s
L_STICK@+100+000 0.1s
"""

BATTLE = """

"""
