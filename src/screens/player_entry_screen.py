"""
src/screens/player_entry_screen.py

See description below.

by Eric Lee, Alex Prosser
10/9/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from .. import common
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import LaserTagSystem

class PlayerEntryColumn(BoxLayout):
    """
    A column for part of the PlayerEntryScreen.

    Takes all the input and stores it in the global state to be used by other parts of the application. 
    """
    def __init__(self, team_name: str):
        super().__init__()
        self.laser_tag_system: LaserTagSystem = None

        self.team_name = team_name
        self.rows: list[tuple[TextInput, TextInput]] = []
        self.row_count = 10
        self.equipment_ids: list[int] = [-1] * self.row_count
        self.create_mode = False
        self.current_player: int = -1

        # setup root ui
        self.orientation = 'vertical'
        self.add_widget(Label(text=f'{self.team_name} Team'))

        # add all the rows
        for i in range(self.row_count):
            row = BoxLayout(orientation='horizontal')
            player_id_input = TextInput(hint_text='Player ID...', multiline=False, size_hint=(0.3, None), height=40, input_filter='int', on_text_validate=self.try_autocomplete)
            player_id_input.row = i
            code_name_input = TextInput(hint_text='Code Name...', multiline=False, size_hint=(0.4, None), height=40, on_text_validate=self.handle_submit)
            code_name_input.row = i
            edit_button = Button(text='Edit', size_hint=(0.3, None), height=40)
            edit_button.bind(on_release=self.handle_submit)
            edit_button.row = i

            row.add_widget(player_id_input)
            row.add_widget(code_name_input)
            row.add_widget(edit_button)

            self.rows.append((player_id_input, code_name_input))
            self.add_widget(row)

        # create equipment id popup
        equipment_id_content = BoxLayout(orientation='vertical')
        
        self.equipment_id_input = TextInput(hint_text='Equipment ID...', multiline=False, input_filter='int', on_text_validate=self.send_equipment_id)
        equipment_id_button = Button(text='Submit', size_hint_y = None, height = 40)
        equipment_id_button.bind(on_release=self.send_equipment_id)
        self.equipment_id_error = Label(text='')

        equipment_id_content.add_widget(Label(text='What equipment ID?:'))
        equipment_id_content.add_widget(self.equipment_id_input)
        equipment_id_content.add_widget(self.equipment_id_error)
        equipment_id_content.add_widget(equipment_id_button)
        self.equipment_id_popup = Popup(title='Set Equipment ID', content=equipment_id_content, size_hint=(0.5, 0.4))

    def clear_table(self):
        """
        Clears all rows and resets the text back
        """
        for player_id_input, code_name_input in self.rows:
            player_id_input.text = ''
            code_name_input.text = ''
            code_name_input.hint_text = 'Code Name...'

    def try_autocomplete(self, instance: Widget):
        """
        Asks the database if the user exists

        If a player ID exists, autocomplete the code name

        If not, ask the user to enter a new code name and create a player

        Also moves the current focus to the code name input
        """
        current_code_name_input: TextInput = self.rows[instance.row][1]
        current_code_name_input.hint_text = 'Searching...'

        player = self.laser_tag_system.supabase.get_player_by_id(id=int(instance.text))
        self.create_mode = (player == None)
        if self.create_mode:
            current_code_name_input.hint_text = 'None found! Please enter new name...'
        else:
            current_code_name_input.text = player['codename']

        current_code_name_input.focus = True

    def handle_submit(self, instance: Widget):
        """
        Creates or updates a player and prompts user to enter a equipment id
        """
        current_player_id_input: TextInput = self.rows[instance.row][0]
        current_code_name_input: TextInput = self.rows[instance.row][1]

        # check to see if player is already in list
        self.current_player = instance.row
        players = self.get_all_players_from_rows()
        error = False
        for i in range(len(players)):
            if (players[i][0] == int(current_player_id_input.text)) and i != self.current_player:
                current_code_name_input.text = ''
                current_code_name_input.hint_text = 'Code Name...'
                current_player_id_input.text = ''

                self.laser_tag_system.show_error('Player already exists!')
                error = True
                break

        # either adds a player's name or update's a players name
        if not error:
            if self.create_mode:
                self.laser_tag_system.supabase.create_player(id=int(current_player_id_input.text), codename=current_code_name_input.text)
            else:
                self.laser_tag_system.supabase.update_player(id=int(current_player_id_input.text), codename=current_code_name_input.text)

            self.equipment_id_input.focus = True
            self.equipment_id_input.text = str(self.equipment_ids[self.current_player])
            self.equipment_id_popup.open()

    def send_equipment_id(self, instance: Widget):
        """
        Sends a UDP request saying that a player has been added

        Also updates global state to create a player
        """
        equipment_id = int(self.equipment_id_input.text)

        if equipment_id in self.equipment_ids:
            self.equipment_id_error.text = 'A player is already attached to this equipment ID!'
        else:
            self.equipment_ids[self.current_player] = equipment_id
            self.laser_tag_system.udp.broadcast(equipment_id)
            self.equipment_id_popup.dismiss()

    def get_all_players_from_rows(self) -> list[common.Player]:
        """
        Gets all the player info from the rows and converts it into useable data

        Will be used to save player info between screens

        Returns:
            list of players from the inputs
        """
        players = []
        for i in range(len(self.rows)):
            player_id_input, code_name_input = self.rows[i]
            if player_id_input.text != '' and code_name_input.text != '':
                players.append((int(player_id_input.text), self.equipment_ids[i], code_name_input.text))
        return players

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code

        Args:
            system: the main LaserTagSystem from main.py
        """
        self.laser_tag_system = system

class PlayerEntryScreen(Screen):
    """
    The player entry screen for the Photon Laser Tag System App.

    This allows for the team's players to be entered into the system.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system: LaserTagSystem = None

        root = BoxLayout(orientation='vertical')

        # create the tables sections
        tables = BoxLayout(orientation='horizontal')
        
        # create red team table
        self.red_team = PlayerEntryColumn(team_name=common.RED_TEAM)
        red_team_layout = BoxLayout(orientation='horizontal', spacing=100)
        red_team_layout.add_widget(self.red_team)

        # create green team table
        self.green_team = PlayerEntryColumn(team_name=common.GREEN_TEAM)
        green_team_layout = BoxLayout(orientation='horizontal', spacing=100)
        green_team_layout.add_widget(self.green_team)

        tables.add_widget(red_team_layout)
        tables.add_widget(green_team_layout)

        root.add_widget(tables)

        # create the button row
        buttons = BoxLayout(orientation='horizontal', height=100, size_hint_y=None)

        clear_button = Button(text='Clear Names', size_hint=(None, None), height=80)
        clear_button.bind(on_release=self.clear_names)

        start_button = Button(text='Start Game', size_hint=(None, None), height=80)
        start_button.bind(on_release=self.start_game)

        buttons.add_widget(clear_button)
        buttons.add_widget(start_button)

        root.add_widget(buttons)

        self.add_widget(root)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code

        Args:
            system: the main LaserTagSystem from main.py
        """
        self.laser_tag_system = system
        self.red_team.set_system(system)
        self.green_team.set_system(system)

    def clear_names(self, instance: Widget):
        """
        Calls both tables clear methods
        """
        self.red_team.clear_table()
        self.green_team.clear_table()

    def start_game(self, instance: Widget):
        """
        Gets all the players from both teams and sends them to global data

        Also checks for duplicates in player and equipment IDs and throws error if found 
        """
        red_players = self.red_team.get_all_players_from_rows()
        green_players = self.green_team.get_all_players_from_rows()

        # check for duplicate players and equipment IDs between teams
        error = False
        for red_player in red_players:
            for green_player in green_players:
                if red_player[0] == green_player[0]:
                    self.laser_tag_system.show_error('There are duplicate players between the teams! FIX IT')
                    error = True
                if red_player[1] == green_player[1]:
                    self.laser_tag_system.show_error('There are duplicate equipment IDs between the teams! FIX IT')
                    error = True

        if not error:
            self.laser_tag_system.players[common.RED_TEAM] = red_players
            self.laser_tag_system.players[common.GREEN_TEAM] = green_players

            self.laser_tag_system.switch_screen(common.COUNTDOWN_SCREEN)
        