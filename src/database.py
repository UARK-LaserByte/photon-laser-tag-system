"""
src/database.py

See description below.

by Alex Prosser, Jackson Morawski
10/1/2023
"""

from supabase import create_client
from dotenv import load_dotenv
import os
from . import common

# load supabase keys (not displayed on github for security reasons)
load_dotenv()

class Supabase():
    """
    This is a wrapper for the Supabase interaction part of the application.\n
    For this, we will probably write any Supabase code here and just give results to whomever call the method
    """
    def __init__(self):
        self.client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

    def get_all_players(self) -> list[dict]:
        response = self.client.table(common.PLAYER_TABLE).select('*').execute()
        return response.data
    
    def get_player_by_id(self, id: int) -> dict | None:
        response = self.client.table(common.PLAYER_TABLE).select('*').eq('id', id).execute()
        if len(response.data) != 0:
            return response.data[0]
        
        return None
    
    def update_player(self, id: int, codename: str):
        self.client.table(common.PLAYER_TABLE).update({'codename': codename}).eq('id', id).execute()

    def create_player(self, id: int, codename: str):
        self.client.table(common.PLAYER_TABLE).insert({'id': id, 'codename': codename}).execute()