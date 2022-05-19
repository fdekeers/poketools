"""
Utilities to connect the virtual controller to the Nintendo Switch.
"""

import nxbt
import time
import threading
from configs import general


class Controller:

    def __init__(self):
        print("Initializing controller...")
        self.nx = nxbt.Nxbt()
        time.sleep(5)  # Add delay for the Raspberry Pi
        self.controller = None

    def synchronize(self):
        """
        connect the controller for the first time
        wait for the user to allow the controller to connect, through the menu
        """
        self.controller = self.nx.create_controller(nxbt.PRO_CONTROLLER)
        print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
        self.nx.wait_for_connection(self.controller)
        print("Pro controller connected !")

    def reconnect(self):
        """
        reconnect the controller if it was not detected any more
        wait for several seconds as the creation of a controller takes some time
        @return: nx, controller
            - nx: Nxbt instance
            - connected controller
        """
        self.controller = self.nx.create_controller(nxbt.PRO_CONTROLLER, reconnect_address=self.nx.get_switch_addresses())
        time.sleep(5)

    def macro(self, macro_str):
        """
        Execute a button macro with this Controller.
        @param macro_str: string representing the macro
        @return: None
        """
        self.nx.macro(self.controller, macro_str)

    def sync_and_go_back(self):
        """
        Synchronize this Controller with a console,
        then execute the macro to go back to the game.
        @return: None
        """
        self.synchronize()
        self.macro(general.GO_BACK_TO_GAME_AFTER_SYNC)

    def busy_wait(self, seconds):
        """
        press several time on the A key to ensure that the controller does not get disconnected
        @param seconds: duration of the busy wait, in seconds
        @return: None. Presses A key several times
        """
        self.macro(general.BUSY_WAIT.format(int(seconds * 5)))

    def busy_wait_b(self, seconds):
        """
        press several time on the N key to ensure that the controller does not get disconnected
        @param seconds: duration of the busy wait, in seconds
        @return: None. Presses B key several times
        """
        self.macro(general.BUSY_WAIT_B.format(int(seconds * 5)))

    def busy_wait_background(self, seconds):
        """
        starts a thread doing a busy wait operation
        @param seconds: duration of the busy wait, in seconds
        @return: None. Presses A key several times
        """
        thread = threading.Thread(target=self.busy_wait, args=[seconds])
        thread.start()

    def reset(self, reset_macro, user):
        """
        Reset the game, with a potential user selection upon starting the game.
        @param reset_macro: macro to reset the game
        @param user: number of the user to use to start the game (0-8)
        @return: None
        """
        self.macro(reset_macro)
        if 1 <= user <= 8:
            # User selection
            self.macro(general.SELECT_USER.format(user-1))

    def run_in_circles(self, steps):
        """
        Execute the macro to run in circle for the given number of steps.
        @param steps: number of steps to complete
        @return: None
        """
        loops = int(steps) - 1
        self.macro(general.STEPS_CIRCLE.format(loops))
