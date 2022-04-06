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
        self.nx.macro(self.controller, macro_str)

    def sync_and_go_back(self):
        self.synchronize()
        self.macro(general.GO_BACK_TO_GAME_AFTER_SYNC)

    def busy_wait(self, seconds):
        """
        press several time on the A key to ensure that the controller does not get disconnected
        @param seconds: duration of the busy wait, in seconds
        @return: None. Presses A key several time
        """
        self.macro(general.BUSY_WAIT.format(int(seconds * 5)))

    def busy_wait_b(self, seconds):
        """
        press several time on the N key to ensure that the controller does not get disconnected
        @param seconds: duration of the busy wait, in seconds
        @return: None. Presses B key several time
        """
        self.macro(general.BUSY_WAIT_B.format(int(seconds * 5)))

    def busy_wait_background(self, seconds):
        """
        starts a thread doing a busy wait operation
        @param seconds:
        @return:
        """
        thread = threading.Thread(target=self.busy_wait, args=seconds)
        thread.start()

    def run_in_circles(self, steps):
        loops = steps  # TODO: adapt loops variable with the number of steps one circle contains
        self.macro(general.STEPS_CIRCLE.format(int(loops)))
