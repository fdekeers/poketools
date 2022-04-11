# Timings
GAME_LOADING_TIME = 36    # Game loading time [s]
BATTLE_LOADING_TIME = 23  # Battle loading time [s]


##########################
# MACROS FOR SHINY RESET #
##########################

START_BATTLE = """
L_STICK@+000+100 1.0s
"""

RESET_GAME = """
HOME 0.05s
0.5s
B 0.1s
0.2s
X 0.1s
0.3s
A 0.1s
1s
A 0.1s
1s
"""