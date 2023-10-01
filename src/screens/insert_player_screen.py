"""
src/screens/player_entry_screen.py

See description below.

by Jackson Morawski
10/1/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from .. import common

class InsertPlayerScreen(Screen):
    """
    The player insert screen for the Photon Laser Tag System App.\n
    This allows for insertion of players into supabase\n
    INCOMPLETE
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system = None

        # create the root UI and add text for now
        root = BoxLayout(orientation='vertical')
    
        root.add_widget(Label(text='Insert Player Screen', font_size=24))
        data_button = Button(text='Go Back', font_size=24)
        data_button.bind(on_press=self.switch_to_player_entry)
        root.add_widget(data_button)
    
        self.add_widget(root)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code
        """
        self.laser_tag_system = system

    def switch_to_player_entry(self, delta_time):
        """
        The callback for the on_enter method which switches the screen to the player entry screen
        """
        self.laser_tag_system.switch_screen(common.PLAYER_ENTRY_SCREEN)

    def get_data(self, instance):
        self.data = self.laser_tag_system.supabase.get_all_players()