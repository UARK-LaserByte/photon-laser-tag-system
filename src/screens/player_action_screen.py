"""
src/screens/player_action_screen.py

See description below.

by Alex Prosser, Eric lee
10/20/2023
"""

import time

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
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
        self.game_time = 10

        # create the root UI and add label for now
        root = BoxLayout(orientation='vertical')
        root.add_widget(Label(text='Player Action Screen'))

        ####

        self.row_count = 10

        teams_layout = GridLayout(cols=2, size_hint=(1, 0.05))
        red_team_label = Label(text="Red Team", size_hint=(1, 0.05))
        green_team_label = Label(text="Green Team", size_hint=(1, 0.05))
        teams_layout.add_widget(red_team_label)
        teams_layout.add_widget(green_team_label)

        names_scores_layout = GridLayout(cols=4, rows= self.row_count, size_hint=(1, 0.6))

        for i in range(self.row_count):
            red_name_label = Label(text= self.laser_tag_system.players[common.RED_TEAM][i], size_hint_x=0.2)
            red_score_label = Label(text=f"Score: 0", size_hint_x=0.1)
            green_name_label = Label(text=self.laser_tag_system.players[common.GREEN_TEAM][i], size_hint_x=0.2)
            green_score_label = Label(text=f"Score: 0", size_hint_x=0.1)
            
            names_scores_layout.add_widget(red_name_label)
            names_scores_layout.add_widget(red_score_label)
            names_scores_layout.add_widget(green_name_label)
            names_scores_layout.add_widget(green_score_label)
        

        self.add_widget(root)

        # Create a ScrollView for the chat log (at the bottom)
        chat_scrollview = ScrollView(size_hint=(1, 0.20))
        chat_logs = TextInput(multiline=True, readonly=True)
        chat_scrollview.add_widget(chat_logs)
        
        layout.add_widget(scores_title)
        layout.add_widget(teams_layout)
        layout.add_widget(names_scores_layout)
        layout.add_widget(chat_scrollview)
    
        ####


    def on_enter(self):
        """
        Sets up main loop to run all UDP actions and update UI accordingly.

        This will run every 1/10 of a second until the game is over

        This is a built-in method from Kivy's Screen class.

        IMCOMPLETE: use UI instead of prints to show actions.
        """

        # send the start signal
        self.laser_tag_system.udp.broadcast(common.UDP_GAME_START)

        self.start_time = time.time()

        self.game_loop = Clock.schedule_interval(self.run_game_loop, 0.1)
        

    def run_game_loop(self, delta_time):
        # receive the data
        id_transmit, id_hit = self.laser_tag_system.udp.try_receive()

        # if there is no errors, process the signal
        if id_transmit != None and id_hit != None:
            hitter = self.laser_tag_system.get_player_by_equipment_id(id=id_transmit)
            hittee = self.laser_tag_system.get_player_by_equipment_id(id=id_hit)

            # Check if a green player has scored on red base
            if id_hit == common.UDP_RED_BASE_SCORED and not hitter[1]:
                chat_logs += f'The green player ' + hitter[0][2] + ' has scored on Red Base!\n'
            # Check if a red player has scored on green base
            elif id_hit == common.UDP_GREEN_BASE_SCORED and hitter[1]:
                chat_logs += f'The red player ' + hitter[0][2] + ' has scored on Green Base!\n'
            # Normal tag
            else:
                chat_logs += f'The player ' + hitter[0][2] + ' has tagged the player ' + hittee[0][2] + '!\n'

            # broadcast whomever was hit
            self.laser_tag_system.udp.broadcast(id_hit)

        # Check if the desired duration has passed
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.game_time:
            # game is now over!
            Clock.unschedule(self.game_loop)

            # send game end signal
            for _ in range(3):
                self.laser_tag_system.udp.broadcast(common.UDP_GAME_END)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code.

        Args:
            system: the main LaserTagSystem from main.py
        """

        self.laser_tag_system = system
