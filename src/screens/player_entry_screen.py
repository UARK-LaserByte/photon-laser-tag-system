"""
src/screens/player_entry_screen.py

See description below.

by Alex Prosser, Eric Lee
9/30/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.textinput import TextInput
from .. import common


class PlayerEntryScreen(Screen):
    """
    The player entry screen for the Photon Laser Tag System App.\n
    This allows for the team's players to be entered into the system.\n
    INCOMPLETE
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system = None

        # create the root UI and add text for now
        root = BoxLayout(orientation='vertical')
    
        root.add_widget(Label(text='Main Menu - Player Entry Screen', font_size=24))
        data_button = Button(text='Get Data', font_size=24)
        data_button.bind(on_press=self.switch_to_player_table)
        root.add_widget(data_button)

        data_button = Button(text='Insert Player', font_size=24)
        data_button.bind(on_press=self.switch_to_insert_player)
        root.add_widget(data_button)
    
        self.add_widget(root)

        ##Eric Lee
        # self.orientation = 'vertical'
        # self.team_name = 'team_name'
        # self.rows = []

        # self.create_header()
        # self.create_header_labels()
        # self.create_rows()
        # self.create_clear_button()

    ##Eric Lee
    # def create_header(self):
    #     header_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
    #     header_label = Label(text=f'{self.team_name} Team', size_hint=(None, 1), width=700)
    #     header_layout.add_widget(header_label)
    #     self.add_widget(header_layout)

    # def create_header_labels(self):
    #     self.header_layout = BoxLayout(orientation='horizontal')
    #     self.header_layout.add_widget(Label(text='Name'))
    #     self.header_layout.add_widget(Label(text='Score'))
    #     self.add_widget(self.header_layout)

    # def create_rows(self):
    #     for _ in range(10):
    #         row_layout = BoxLayout(orientation='horizontal')
    #         name_input = TextInput(hint_text='', multiline=False)
    #         score_input = TextInput(hint_text='', multiline=False, disabled=True)

    #         row_layout.add_widget(name_input)
    #         row_layout.add_widget(score_input)

    #         self.rows.append((name_input, score_input))
    #         self.add_widget(row_layout)

    # def create_clear_button(self):
    #     clear_button = Button(text='Clear Names', size_hint=(None, None), size=(400, 80))
    #     clear_button.bind(on_release=self.clear_names)
    #     self.add_widget(clear_button)

    # def clear_names(self, instance):
    #     for name_input, _ in self.rows:
    #         name_input.text = ''

    # def update_table(self):
    #     # Print or process the data for the team here
    #     print(f'{self.team_name} Team:')
    #     for i, (name_input, score_input) in enumerate(self.rows, 1):
    #         name = name_input.text
    #         score = score_input.text
    #         print(f'Player {i}: Name={name}, Score={score}')
    # ##

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code
        """
        self.laser_tag_system = system

    # def get_data(self, instance):
    #     self.data = self.laser_tag_system.supabase.get_all_players()

    def switch_to_player_table(self, delta_time):
        """
        The callback for the on_enter method which switches the screen to the player entry screen
        """
        self.laser_tag_system.switch_screen(common.PLAYER_TABLE_SCREEN)

    def switch_to_insert_player(self, delta_time):
        """
        The callback for the on_enter method which switches the screen to the player entry screen
        """
        self.laser_tag_system.switch_screen(common.INSERT_PLAYER_SCREEN)
    def get_data(self, instance):
        self.laser_tag_system.supabase.get_all_players()
    
    ##Eric Lee
    # class TeamScoreScreen(App):
    #     def build(self):
    #         self.red_team_table = PlayerEntryScreen(team_name='Red')
    #         self.green_team_table = PlayerEntryScreen(team_name='Green')

    #         main_layout = BoxLayout(orientation='horizontal')
    #         main_layout.add_widget(self.red_team_table)
    #         main_layout.add_widget(self.green_team_table)

    #         return main_layout
    ##
    # if __name__ == '__main__':
    #     TeamScoreScreen().run()
