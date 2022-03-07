import audio
import nxbt
import time
import macros
import threading


def synchronize_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER)
    print('Please go to the "Change Grip/Order" menu of your Nintendo Switch, to connect the virtual controller.')
    nx.wait_for_connection(controller)
    print("Pro controller connected !")
    return controller


def reconnect_controller(nx):
    controller = nx.create_controller(nxbt.PRO_CONTROLLER,
                                      reconnect_address=nx.get_switch_addresses())
    time.sleep(5)
    return controller


def busy_wait(controller, seconds):
    iterations = int(seconds * 5)
    nx.macro(controller, macros.BUSY_WAIT.format(iterations))


def busy_wait_background(controller, seconds):
    thread = threading.Thread(target=busy_wait, args=(controller, seconds))
    thread.start()


if __name__ == "__main__":
    # Initialize and connect virtual game controller, then go back to game
    print("Initializing...")
    nx = nxbt.Nxbt()
    time.sleep(5)  # Add delay for the Raspberry Pi
    controller = synchronize_controller(nx)
    nx.macro(controller, macros.GO_BACK_TO_GAME_AFTER_SYNC)

    nx.macro(controller, macros.STEPS_RECHARGE)
