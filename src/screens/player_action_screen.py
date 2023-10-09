"""
src/screens/player_action_screen.py

See description below.

by Alex Prosser
10/9/2023
"""

import time

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from .. import common
from typing import TYPE_CHECKING

# to prevent circle imports
if TYPE_CHECKING:
    from main import LaserTagSystem

class PlayerActionScreen(Screen):
    """
    The player action screen shows the list of red and green players and all the actions that happen.

    This is built off of Kivy's built-in Screen system.

    INCOMPLETE: no UI is implemented, but the UDP is.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system: LaserTagSystem = None

        self.game_running = True
        self.game_time = 60

        # create the root UI and add label for now
        root = BoxLayout(orientation='vertical')
        root.add_widget(Label(text='Player Action Screen'))
        self.add_widget(root)

    def on_enter(self):
        """
        Sets up main loop to run all UDP actions and update UI accordingly.

        This is a built-in method from Kivy's Screen class.

        IMCOMPLETE: use UI instead of prints to show actions.
        """

        # send the start signal
        self.laser_tag_system.udp.broadcast(common.UDP_GAME_START)

        self.start_time = time.time()
        while self.game_running:
            # receive the data
            id_transmit, id_hit = self.laser_tag_system.udp.try_receive()

            # if there is no errors, process the signal
            if id_transmit != None and id_hit != None:
                hitter = self.laser_tag_system.get_player_by_equipment_id(id=id_transmit)
                hittee = self.laser_tag_system.get_player_by_equipment_id(id=id_hit)

                # Check if a green player has scored on red base
                if id_hit == common.UDP_RED_BASE_SCORED and not hitter[1]:
                    print('The green player ' + hitter[0][2] + ' has scored on Red Base!')
                # Check if a red player has scored on green base
                elif id_hit == common.UDP_GREEN_BASE_SCORED and hitter[1]:
                    print('The red player ' + hitter[0][2] + ' has scored on Green Base!')
                # Normal tag
                else:
                    print('The player ' + hitter[0][2] + ' has tagged the player ' + hittee[0][2] + '!')

                # broadcast whomever was hit
                self.laser_tag_system.udp.broadcast(id_hit)

            # Check if the desired duration has passed
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.game_time:
                self.game_running = False

                # send game end signal
                for _ in range(3):
                    self.laser_tag_system.udp.broadcast(common.UDP_GAME_END)
            else:
                self.update_ui()

    def update_ui(self):
        """
        Update the UI anytime this is called.

        INCOMPLETE: No UI to be updated just yet.
        """
        pass

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code.

        Args:
            system: the main LaserTagSystem from main.py
        """

        self.laser_tag_system = system