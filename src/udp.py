"""
src/udp.py

See description below.

by Alex Prosser
11/14/2023
"""

import socket
from . import common


class UDP:
    """
    This is a wrapper for the UDP interaction part of the application.

    For this, we will probably write any UDP code here and just give results to whomever call the method.
    """

    def __init__(self):
        # Create a UDP sockets
        self.socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_receive.settimeout(
            0.1
        )  # Stop trying after 0.1 seconds to run other code

        # Bind receive UDP to localhost:7501
        self.socket_receive.bind((common.URL_LOCALHOST, common.PORT_SOCKET_RECEIVE))

    def try_receive(self) -> tuple[int, int] | None:
        """
        Try to receive data from the UDP receive channel

        Returns:
            tuple with transmitter ID and hit ID if data was received; None is no data was received
        """

        try:
            # Receive any data that might have come in
            data, _ = self.socket_receive.recvfrom(common.SOCKET_BUFFER_SIZE)
            id_transmit, id_hit = map(lambda id: int(id), data.decode().split(":"))
            return (id_transmit, id_hit)
        except socket.timeout:
            # No data has come in, try again
            return None

    def broadcast(self, message: int):
        """
        Broadcast a message to all the devices on the broadcast UDP channel

        Args:
            message: an integer to send (most likely a equipment ID)
        """

        self.socket_broadcast.sendto(
            str.encode(str(message)),
            (common.URL_LOCALHOST, common.PORT_SOCKET_BROADCAST),
        )
