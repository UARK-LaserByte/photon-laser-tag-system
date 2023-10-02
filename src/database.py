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
load_dotenv(r) # r"PATH TO ENV"

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
    
    def submit_data(data):
        id = data.id_input.text
        first_name = data.first_name_input.text
        last_name = data.last_name_input.text
        codename = data.codename_input.text

        # Insert data into the 'player' table
        data_to_insert = [{'id': id, 'first_name': first_name, 'last_name': last_name, 'codename': codename}]
        error = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')).table('player').upsert(data_to_insert).execute()
        if error:
            print('Error:', error)
        else:
            print('Data inserted/updated successfully!')


