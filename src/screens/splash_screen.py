"""
src/screens/splash_screen.py

See description below.

by Cindy Nguyen, Alex Prosser
10/22/2023
"""

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from .. import common
from typing import TYPE_CHECKING

# to prevent circle imports
if TYPE_CHECKING:
    from main import LaserTagSystem


class SplashScreen(Screen):
    """
    The splash screen shows the photon logo for 3 seconds, then moves to the player entry screen.

    This is built off of Kivy's built-in Screen system.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system: LaserTagSystem = None

        # create the root UI and add image
        root = BoxLayout(orientation="vertical")
        image = Image(source="resources/logo.jpg")
        fade_animation = Animation(opacity=0, duration=3)
        fade_animation.start(image)

        root.add_widget(image)
        self.add_widget(root)

    def on_enter(self):
        """
        Sets up timer to switch to player entry screen after 3 seconds.

        This is a built-in method from Kivy's Screen class and uses the Clock class.

        BUG: The Supabase client initialization delays the loading of UI, so it needs to take longer (hence, SUPABASE_DELAY)
        """

        SUPABASE_DELAY = 2
        Clock.schedule_once(self.switch_to_player_entry, 3 + SUPABASE_DELAY)

    def switch_to_player_entry(self, delta_time):
        """
        The callback for the on_enter method which switches the screen to the player entry screen
        """

        self.laser_tag_system.switch_screen(common.PLAYER_ENTRY_SCREEN)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code

        Args:
            system: the main LaserTagSystem from main.py
        """

        self.laser_tag_system = system
