"""
src/screens/player_action_screen.py

See description below.

by Eric Lee, Alex Prosser
11/14/2023
"""

import time
import random

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from .. import common
from typing import TYPE_CHECKING

# to prevent circle imports
if TYPE_CHECKING:
    from main import LaserTagSystem


class PlayerActionScreen(Screen):
    """
    The player action screen shows the list of red and green players and all the actions that happen.

    This is built off of Kivy's built-in Screen system.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system: LaserTagSystem = None

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.game_running = True
        self.game_time = 10  # switch to 360 for final submission

        root = BoxLayout(orientation="vertical")

        # add team labels
        teams_layout = GridLayout(cols=2, size_hint=(1, 0.1))
        self.red_team_label = Label(
            text=f"{common.RED_TEAM} Team - Total Score: 0", size_hint=(1, 0.1)
        )
        self.green_team_label = Label(
            text=f"{common.GREEN_TEAM} Team - Total Score: 0", size_hint=(1, 0.1)
        )
        teams_layout.add_widget(self.red_team_label)
        teams_layout.add_widget(self.green_team_label)

        # add player's scoreboard
        players_scoreboard = GridLayout(cols=2, size_hint=(1, 0.5))
        self.red_players = BoxLayout(orientation="vertical")
        self.green_players = BoxLayout(orientation="vertical")
        players_scoreboard.add_widget(self.red_players)
        players_scoreboard.add_widget(self.green_players)

        # add chat log
        chat_scrollview = ScrollView(size_hint=(1, 0.4))
        self.chat_logs = TextInput(multiline=True, readonly=True)
        chat_scrollview.add_widget(self.chat_logs)

        root.add_widget(teams_layout)
        root.add_widget(players_scoreboard)
        root.add_widget(chat_scrollview)

        self.add_widget(root)

    def on_enter(self):
        """
        Sets up main loop to run all UDP actions and update UI accordingly.

        This will run every 1/10 of a second until the game is over

        This is a built-in method from Kivy's Screen class.
        """

        # send the start signal and start the board
        self.laser_tag_system.udp.broadcast(common.UDP_GAME_START)
        self.start_time = time.time()
        self.update_players()
        self.game_running = True
        self.chat_logs.text = ""
        random.choice(self.laser_tag_system.music).play()

        self.game_loop = Clock.schedule_interval(self.run_game_loop, 0.1)

    def run_game_loop(self, delta_time: float):
        """
        Receives all UDP data and updates player accordingly

        Handles score and 'base' touching
        """
        # receive the data
        results = self.laser_tag_system.udp.try_receive()

        # if there is no errors, process the signal
        if results != None:
            hitter = self.laser_tag_system.get_player_by_equipment_id(
                id=results[0])
            hittee = self.laser_tag_system.get_player_by_equipment_id(
                id=results[1])

            # Check if a green player has scored on red base
            if (
                results[1] == common.UDP_RED_BASE_SCORED
                and hitter.team == common.GREEN_TEAM
            ):
                hitter.score += 100
                hitter.reached_base = True
                self.chat_logs.text += (
                    f"The green player {hitter.codename} has scored on Red Base!\n"
                )
            # Check if a red player has scored on green base
            elif (
                results[1] == common.UDP_GREEN_BASE_SCORED
                and hitter.team == common.RED_TEAM
            ):
                hitter.score += 100
                hitter.reached_base = True
                self.chat_logs.text += (
                    f"The red player {hitter.codename} has scored on Green Base!\n"
                )
            # Normal tag
            else:
                hitter.score += 10
                if hittee.team == hitter.team:
                    self.chat_logs.text += f"The player {hitter.codename} has tagged the player {hittee.codename}! Friendly fire!\n"
                    # broadcast hitter
                    self.laser_tag_system.udp.broadcast(results[0])
                else:
                    self.chat_logs.text += f"The player {hitter.codename} has tagged the player {hittee.codename}!\n"
                    # broadcast hittee
                    self.laser_tag_system.udp.broadcast(results[1])

            self.update_players()

        # Check if the desired duration has passed
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.game_time:
            # game is now over!
            Clock.unschedule(self.game_loop)
            self.game_running = False
            self.chat_logs.text += "Game over! Press F5 to go back to entry screen!"

            # send game end signal
            for _ in range(3):
                self.laser_tag_system.udp.broadcast(common.UDP_GAME_END)

    def update_players(self):
        """
        Adds all players to their according team's column in the players_scoreboard widget
        """

        # reset all scoreboard widgets
        self.red_players.clear_widgets()
        self.green_players.clear_widgets()

        red_score = 0

        # add all red players
        for red_player in sorted(
            self.laser_tag_system.players[common.RED_TEAM],
            key=lambda player: player.score,
            reverse=True,
        ):
            base = ""
            if red_player.reached_base:
                base = "B"

            red_player_row = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=40
            )
            red_player_row.add_widget(
                Label(text=base, size_hint=(0.2, None))
            )  # Base Indicator (not needed yet)
            red_player_row.add_widget(
                Label(text=red_player.codename, size_hint=(0.6, None))
            )  # Name
            red_player_row.add_widget(
                Label(text=str(red_player.score), size_hint=(0.2, None))
            )  # Score

            self.red_players.add_widget(red_player_row)

            red_score += red_player.score

        self.red_team_label.text = f"{common.RED_TEAM} Team - Total Score: {red_score}"

        green_score = 0

        # add all green players
        for green_player in sorted(
            self.laser_tag_system.players[common.GREEN_TEAM],
            key=lambda player: player.score,
            reverse=True,
        ):
            base = ""
            if green_player.reached_base:
                base = "B"

            green_player_row = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=40
            )
            green_player_row.add_widget(
                Label(text=base, size_hint=(0.2, None))
            )  # Base Indicator (not needed yet)
            green_player_row.add_widget(
                Label(text=green_player.codename, size_hint=(0.6, None))
            )  # Name
            green_player_row.add_widget(
                Label(text=str(green_player.score), size_hint=(0.2, None))
            )  # Score

            self.green_players.add_widget(green_player_row)

            green_score += green_player.score

        self.green_team_label.text = (
            f"{common.GREEN_TEAM} Team - Total Score: {green_score}"
        )

        # aligns all rows to the top
        self.red_players.add_widget(Widget())
        self.green_players.add_widget(Widget())

    def _keyboard_closed(self):
        print("keyboard closed!")

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "escape":
            self._keyboard.unbind(
                on_key_down=self._on_keyboard_down)  # fricked up here
            self._keyboard = None
            keyboard.release()
        if keycode[1] == "f5" and not self.game_running:
            self.laser_tag_system.switch_screen(common.PLAYER_ENTRY_SCREEN)

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code

        Args:
            system: the main LaserTagSystem from main.py
        """

        self.laser_tag_system = system
