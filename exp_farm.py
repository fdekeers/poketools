import time
from utils.controller import Controller
from configs import general
import threading


if __name__ == "__main__":
    # Initialize and connect virtual game controller, then go back to game
    controller = Controller()
    controller.sync_and_go_back()

    controller.run_in_circles(100)
