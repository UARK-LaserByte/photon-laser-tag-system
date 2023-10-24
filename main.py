"""
main.py

This is the main application where we actually use all the code to create the application.
Right now, it isn't super complicated as we are on Sprint #3, which doesn't implement the full thing yet.

by Alex Prosser, Jackson Morawski
10/9/2023
"""

# kivy imports
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget

# own imports
from src import common
from src.database import Supabase
from src.udp import UDP
from src.screens.player_entry_screen import PlayerEntryScreen
from src.screens.splash_screen import SplashScreen
from src.screens.countdown_screen import CountdownScreen
from src.screens.player_action_screen import PlayerActionScreen

# hide window so it doesn't look as weird
Window.hide()

class LaserTagSystem(App):
    """
    The starting point for the Photon Laser Tag System App.

    Creates all screens and handlers to operate the application.

    Built off of Kivy's App class to be cross-platform.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # other systems
        self.supabase = Supabase()
        self.udp = UDP()

        # state management system
        self.players: dict[str, list[common.Player]] = { common.RED_TEAM: [], common.GREEN_TEAM: [] }

        # create main screen manager and add all current screens to it
        self.screen_manager = ScreenManager()

        self.splash_screen = SplashScreen(name=common.SPLASH_SCREEN)
        self.splash_screen.set_system(self)
        self.player_entry_screen = PlayerEntryScreen(name=common.PLAYER_ENTRY_SCREEN)
        self.player_entry_screen.set_system(self)
        self.countdown_screen = CountdownScreen(name=common.COUNTDOWN_SCREEN)
        self.countdown_screen.set_system(self)
        self.player_action_screen = PlayerActionScreen(name=common.PLAYER_ACTION_SCREEN)
        self.player_action_screen.set_system(self)
        
        self.screen_manager.add_widget(self.splash_screen)
        self.screen_manager.add_widget(self.player_entry_screen)
        self.screen_manager.add_widget(self.countdown_screen)
        self.screen_manager.add_widget(self.player_action_screen)

        # create error popup
        error_content = BoxLayout(orientation='vertical')
        
        error_button = Button(text='Dismiss', size_hint_y=None, height=40)
        error_button.bind(on_release=self.dismiss_error)

        self.error_message_label = Label(text='No error...')
        error_content.add_widget(self.error_message_label)
        error_content.add_widget(error_button)
        self.error_popup = Popup(title='Error', content=error_content, size_hint=(0.5, 0.4))

    def on_start(self):
        """
        Sets up all the necessary classes that are needed to run the app.

        This is a built-in method from Kivy's App class.
        """
    
        # setup and show window to the correct size and title
        Window.size = (common.WINDOW_WIDTH, common.WINDOW_HEIGHT)
        Window.set_title(common.WINDOW_TITLE)
        Window.show()

        # setup handlers for input and database
        self.keyboard_manager = Window.request_keyboard(self.close_keyboard, self.root)

        # set splash screen as first screen to be displayed
        self.switch_screen(common.SPLASH_SCREEN)

    def get_player_by_equipment_id(self, id: int) -> tuple[common.Player, bool] | None:
        """
        Get a player from the current global state by their equipment id.

        Args:
            id: equipment id used to search

        Returns:
            tuple with Player and team (True for red, False for green) if found; None if no player found 
        """

        # search red players
        for red_player in self.players[common.RED_TEAM]:
            if red_player[1] == id:
                return (red_player, True)
            
        # search green players
        for green_player in self.players[common.GREEN_TEAM]:
            if green_player[1] == id:
                return (green_player, False)

        return None 

    def build(self):
        """
        Renders the screen manager to the window to allow use of the Screen system.

        This is a built-in method from Kivy's App class.
        """

        return self.screen_manager
    
    def close_keyboard(self):
        """
        Clean up keyboard handler when we close the app.
        """

        self.keyboard_manager = None

    def switch_screen(self, screen_name: str):
        """
        Switches the screen to the screen specified.
        
        Args:
            screen_name: screen id defined in src/common.py
        """

        self.screen_manager.current = screen_name

    def dismiss_error(self, instance: Widget):
        """
        Callback to the error popup which closes it
        """

        self.error_popup.dismiss()

    def show_error(self, message: str):
        """
        Updates popup with new error message and shows it

        Args:
            message: error message to show
        """
        
        self.error_message_label.text = message
        self.error_popup.open()

# create laser tag system in the global scope so all screens has access to it
laser_tag_system = LaserTagSystem()

# run app if we are running the file itself
if __name__ == "__main__":
    laser_tag_system.run()