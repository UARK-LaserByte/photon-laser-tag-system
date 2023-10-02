"""
src/udp.py

See description below.

by Alex Prosser
10/1/2023
"""

import socket
from . import common

class UDP():
    """
    This is a wrapper for the UDP interaction part of the application.\n
    For this, we will probably write any UDP code here and just give results to whomever call the method\n
    For sprint 2, we don't need any receiving code, so this is all we are doing right now
    """
    def __init__(self):
        # Create a UDP sockets
        self.socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def broadcast(self, message: int):
        self.socket_broadcast.sendto(str.encode(str(message)), (common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST))