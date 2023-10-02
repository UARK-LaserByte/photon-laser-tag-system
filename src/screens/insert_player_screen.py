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
from ..database import Supabase
from kivy.uix.textinput import TextInput

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
    
        instance = Supabase

        root.orientation = 'vertical'

        self.id_input = TextInput(hint_text='Enter ID')
        self.first_name_input = TextInput(hint_text='Enter First Name')
        self.last_name_input = TextInput(hint_text='Enter Last Name')
        self.codename_input = TextInput(hint_text='Enter Codename')

        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_release=self.submit_data) 

        root.add_widget(self.id_input)
        root.add_widget(self.first_name_input)
        root.add_widget(self.last_name_input)
        root.add_widget(self.codename_input)
        root.add_widget(self.submit_button)

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

    def submit_data(self, instance):
        Supabase.submit_data(self)