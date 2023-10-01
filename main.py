"""
main.py

This is the main application where we actually use all the code to create the application.
Right now, it isn't super complicated as we are on Sprint #2, which doesn't implement the full thing yet.

by Alex Prosser, Jackson Morawski
9/28/2023
"""

# kivy imports
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

# own imports
from src import common
from src.database import Supabase
from src.screens.player_entry_screen import PlayerEntryScreen
from src.screens.splash_screen import SplashScreen
from src.screens.player_table_screen import PlayerTableScreen
from src.screens.insert_player_screen import InsertPlayerScreen

# hide window so it doesn't look as weird
Window.hide()

class LaserTagSystem(App):
    """
    The starting point for the Photon Laser Tag System App.\n
    Creates all screens and handlers to operate the application.
    Built off of Kivy's App class to be cross-platform.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create main screen manager and add all current screens to it
        self.screen_manager = ScreenManager()
        self.supabase = Supabase()

        self.splash_screen = SplashScreen(name=common.SPLASH_SCREEN)
        self.splash_screen.set_system(self)
        self.player_entry_screen = PlayerEntryScreen(name=common.PLAYER_ENTRY_SCREEN)
        self.player_entry_screen.set_system(self)
        self.player_table_screen = PlayerTableScreen(name=common.PLAYER_TABLE_SCREEN)
        self.player_table_screen.set_system(self)
        self.insert_player_screen = InsertPlayerScreen(name=common.INSERT_PLAYER_SCREEN)
        self.insert_player_screen.set_system(self)
        
        self.screen_manager.add_widget(self.splash_screen)
        self.screen_manager.add_widget(self.player_entry_screen)
        self.screen_manager.add_widget(self.player_table_screen)
        self.screen_manager.add_widget(self.insert_player_screen)

    def on_start(self):
        """
        Sets up all the necessary classes that are needed to run the app.
        This is a built-in method from Kivy's App class\n
        """
        
        # setup and show window to the correct size and title
        Window.size = (common.WINDOW_WIDTH, common.WINDOW_HEIGHT)
        Window.set_title(common.WINDOW_TITLE)
        Window.show()

        # setup handlers for input and database
        self.keyboard_manager = Window.request_keyboard(self.close_keyboard, self.root)

        # set splash screen as first screen to be displayed
        self.switch_screen(common.SPLASH_SCREEN)

    def build(self):
        """
        Renders the screen manager to the window to allow use of the Screen system.\n
        This is a built-in method from Kivy's App class
        """
        return self.screen_manager
    
    def close_keyboard(self):
        """
        Clean up keyboard handler when we close the app.
        """
        self.keyboard_manager = None

    def switch_screen(self, screen_name):
        """
        Switches the screen using the screen id. 
        """
        self.screen_manager.current = screen_name

# create laser tag system in the global scope so all screens has access to it
laser_tag_system = LaserTagSystem()

# run app if we are running the file itself
if __name__ == "__main__":
    laser_tag_system.run()