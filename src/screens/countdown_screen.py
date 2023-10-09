"""
src/screens/countdown_screen.py

See description below.

by Alex Prosser
10/9/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from .. import common
from typing import TYPE_CHECKING

# to prevent circle imports
if TYPE_CHECKING:
    from main import LaserTagSystem

class CountdownScreen(Screen):
    """
    The countdown screen shows a timer, then moves the player action screen.
    
    This is built off of Kivy's built-in Screen system.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system: LaserTagSystem = None

        self.time_left = 5

        # create the root UI and add label and basic timer for now
        root = BoxLayout(orientation='vertical')
        
        self.timer_label = Label(text=f'Time Remaining: {self.time_left} seconds')
        
        root.add_widget(Label(text='Countdown Screen'))
        root.add_widget(self.timer_label)
        
        self.add_widget(root)

    def on_enter(self):
        """
        Sets up timer to run each second and check for the end of the timer

        This is a built-in method from Kivy's Screen class and uses the Clock class
        """

        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, delta_time):
        """
        Updates the countdown timer and switches to the player action screen after
        """

        self.time_left -= 1

        # switch when the timer reaches 0
        if self.time_left <= 0:
            self.time_left = 0
            Clock.unschedule(self.timer_event)
            self.laser_tag_system.switch_screen(common.PLAYER_ACTION_SCREEN)

        self.timer_label.text = f'Time Remaining: {self.time_left} seconds'

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code

        Args:
            system: the main LaserTagSystem from main.py
        """

        self.laser_tag_system = system