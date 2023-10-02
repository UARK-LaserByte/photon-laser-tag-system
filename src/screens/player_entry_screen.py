"""
src/screens/player_entry_screen.py

See description below.

by Eric Lee, Alex Prosser
10/1/2023
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class PlayerEntryColumn(BoxLayout):
    def __init__(self, team_name):
        super().__init__()
        self.laser_tag_system = None

        self.orientation = 'vertical'
        self.team_name = team_name
        self.rows = []
        self.create = False
        
        equipment_id_content = BoxLayout(orientation='vertical')
        
        self.equipment_id_input = TextInput(hint_text='Equipment ID...', multiline=False, input_filter='int', on_text_validate=self.send_equipment_id)
        equipment_id_button = Button(text='Submit', size_hint_y = None, height = 40)
        equipment_id_button.bind(on_release=self.send_equipment_id)

        equipment_id_content.add_widget(Label(text='What equipment ID?:'))
        equipment_id_content.add_widget(self.equipment_id_input)
        equipment_id_content.add_widget(equipment_id_button)
        self.equipment_id_popup = Popup(title='Set Equipment ID', content=equipment_id_content, size_hint=(0.5, 0.3))

        self.add_widget(Label(text=f'{self.team_name} Team'))

        for _ in range(10):
            row = BoxLayout(orientation='horizontal')
            player_id_input = TextInput(hint_text='Player ID...', multiline=False, size_hint=(0.3, None), height=40, input_filter='int', on_text_validate=self.try_autocomplete)
            code_name_input = TextInput(hint_text='Code Name...', multiline=False, size_hint=(0.4, None), height=40, on_text_validate=self.handle_submit)
            edit_button = Button(text='Edit', size_hint=(0.3, None), height=40)
            edit_button.bind(on_release=self.handle_submit)

            row.add_widget(player_id_input)
            row.add_widget(code_name_input)
            row.add_widget(edit_button)

            self.rows.append((player_id_input, code_name_input))
            self.add_widget(row)

    def clear_table(self):
        for player_id_input, code_name_input in self.rows:
            player_id_input.text = ''
            code_name_input.text = ''
            code_name_input.hint_text = 'Code Name...'

    def try_autocomplete(self, instance):
        current_code_name_input = instance.parent.children[1] # get the other TextInput
        current_code_name_input.hint_text = 'Searching...'

        player = self.laser_tag_system.supabase.get_player_by_id(id=int(instance.text))
        if player != None:
            current_code_name_input.text = player['codename']
            self.create = False
        else:
            current_code_name_input.hint_text = 'None found! Please enter new name...'
            self.create = True

    def handle_submit(self, instance):
        if self.create:
            self.create_player(instance)
        else:
            self.submit_player(instance)

    def create_player(self, instance):
        current_code_name_input = instance.parent.children[1]
        current_player_id_input = instance.parent.children[2]
        self.laser_tag_system.supabase.create_player(id=int(current_player_id_input.text), codename=current_code_name_input.text)
        self.equipment_id_popup.open()

    def submit_player(self, instance):
        current_code_name_input = instance.parent.children[1]
        current_player_id_input = instance.parent.children[2]
        self.laser_tag_system.supabase.update_player(id=int(current_player_id_input.text), codename=current_code_name_input.text)
        self.equipment_id_popup.open()

    def send_equipment_id(self, instance):
        self.laser_tag_system.udp.broadcast(int(self.equipment_id_input.text))
        self.equipment_id_popup.dismiss()

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code
        """
        self.laser_tag_system = system

class PlayerEntryScreen(Screen):
    """
    The player entry screen for the Photon Laser Tag System App.\n
    This allows for the team's players to be entered into the system.\n
    INCOMPLETE
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.laser_tag_system = None

        root = BoxLayout(orientation='vertical')
        table = BoxLayout(orientation='horizontal')

        self.red_team = PlayerEntryColumn(team_name='Red')
        red_team_layout = BoxLayout(orientation='horizontal', spacing=100)
        red_team_layout.add_widget(self.red_team)

        self.green_team = PlayerEntryColumn(team_name='Green')
        green_team_layout = BoxLayout(orientation='horizontal', spacing=100)
        green_team_layout.add_widget(self.green_team)

        table.add_widget(red_team_layout)
        table.add_widget(green_team_layout)
        root.add_widget(table)

        clear_button = Button(text='Clear Names', size_hint=(None, None))
        clear_button.bind(on_release=self.clear_names)
        root.add_widget(clear_button)

        self.add_widget(root)

    def set_system(self, system):
        """
        Sets the main system to make global calls to the other parts of the code
        """
        self.laser_tag_system = system
        self.red_team.set_system(system)
        self.green_team.set_system(system)

    def clear_names(self, instance):
        self.red_team.clear_table()
        self.green_team.clear_table()