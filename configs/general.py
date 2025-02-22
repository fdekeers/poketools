# Macros used in any scenario

##################
# GENERAL MACROS #
##################

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

SELECT_USER = """
LOOP {}
    DPAD_RIGHT 0.1s
    0.2s
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


#########################################
# MACROS FOR CAPTURING SCREENSHOT/VIDEO #
#########################################

SCREENSHOT = """
CAPTURE 0.1s
"""

VIDEO = """
CAPTURE 1.0s
"""


##################################
# MACROS FOR MASUDA AND EXP FARM #
##################################

GET_ON_BIKE = """
PLUS 0.1s
0.5s
DPAD_RIGHT 0.1s
0.5s
"""

STEPS_CIRCLE = """
L_STICK@+100+000 0.4s
L_STICK@+000+100 0.08s
L_STICK@-100+000 0.08s
L_STICK@+000-100 0.08s
LOOP {}
    L_STICK@+100+000 0.08s
    L_STICK@+000+100 0.08s
    L_STICK@-100+000 0.08s
    L_STICK@+000-100 0.08s
L_STICK@+000+000 0.1s
"""

EGG_HATCHING = """
A 0.1s
"""

RELEASE_BREEDJECT = """
X 0.1s
0.2s
DPAD_RIGHT 0.1s
0.1s
A 0.1s
0.5s
R 0.1s
0.5s
"""

GET_NEW_EGG = """
"""

#######################
# MACROS FOR EXP FARM #
#######################

BATTLE = """

"""