"""
src/screens/player_action_screen.py

See description below.

by Alex Prosser
10/7/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class PlayerActionScreen(Screen):
    """
    The player action screen shows the list of red and green players and all the actions that happen.\n
    This is built off of Kivy's built-in Screen system.
    INCOMPLETE: no actions are expected yet, so just implement the players
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system = None

        # create the root UI and add label for now
        root = BoxLayout(orientation='vertical')
        root.add_widget(Label(text='Player Action Screen'))
        self.add_widget(root)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code
        """
        self.laser_tag_system = system