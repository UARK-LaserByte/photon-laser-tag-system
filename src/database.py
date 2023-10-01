"""
src/database.py

See description below.

by Alex Prosser, Jackson Morawski
9/28/2023
"""

from supabase import create_client
from dotenv import load_dotenv
import os
from . import common

# load supabase keys (not displayed on github for security reasons)
load_dotenv(r"Path To .Env") # r"PATH TO ENV"

class Supabase():
    """
    This is a wrapper for the Supabase interaction part of the application.\n
    For this, we will probably write any Supabase code here and just give results to whomever call the method
    """
    def __init__(self):
        self.client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

    def get_all_players(self) -> list[dict]:
        response = self.client.from_('player').select('*').execute()
        return response.data

    # def display_data(self, data):
    #     layout = BoxLayout(orientation='vertical')
        
    #     # Iterate over the data and create labels to display it
    #     for row in data:
    #         label_text = f"ID: {row['id']}, Name: {row['first_name']} {row['last_name']}, Codename: {row['codename']}"
    #         label = Label(text=label_text)
    #         layout.add_widget(label)

    #     # Add a button to go back to the enter_data screen
    #     back_button = Button(text="Back to Enter Data")
    #     back_button.bind(on_release=self.go_to_enter_data)
    #     layout.add_widget(back_button)

    #     self.add_widget(layout)


