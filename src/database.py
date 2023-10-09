"""
src/database.py

See description below.

by Jackson Morawski, Alex Prosser
10/9/2023
"""

from supabase import create_client
from dotenv import load_dotenv
import os
from . import common

# load supabase keys (not displayed on github for security reasons)
load_dotenv()

class Supabase():
    """
    This is a wrapper for the Supabase interaction part of the application.
    
    For this, we will probably write any Supabase code here and just give results to whomever call the method
    """
    def __init__(self):
        self.client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    def get_player_by_id(self, id: int) -> dict | None:
        """
        Gets a specific player from an ID

        Args:
            id: player ID to search for

        Returns:
            the data about the player as { 'id': <id>, 'codename': <name> } 
        """

        response = self.client.table(common.PLAYER_TABLE).select('*').eq('id', id).execute()
        if len(response.data) != 0:
            return response.data[0]
        
        return None
    
    def update_player(self, id: int, codename: str):
        """
        Updates a player's codename using an id

        Args:
            id: player ID to update
            codename: updated player's codename 
        """

        self.client.table(common.PLAYER_TABLE).update({'codename': codename}).eq('id', id).execute()

    def create_player(self, id: int, codename: str):
        """
        Creates a new player from an ID and codename

        Args:
            id: player ID
            codename: player's codename
        """
        
        self.client.table(common.PLAYER_TABLE).insert({'id': id, 'codename': codename}).execute()