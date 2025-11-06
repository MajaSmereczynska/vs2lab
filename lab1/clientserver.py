"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

        # In-memory telephone directory
        self.directory = {
            "Alpha": "1234567890",
            "Bravo": "2345678901",
            "Charlie": "3456789012"
        }

    def close(self):
        self.sock.close()
        self.logger.info("Server down.")

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        connection = None
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                self._logger.info(f"Connection accepted from {address}")   
                while True:  # forever
                    try:
                        data = connection.recv(1024).decode('utf-8')
                        self._logger.info(f"Received data: {data}")
                        if not data:
                            self._logger.info("Client disconnected")
                            break  # Client has closed the connection
                        if data.startswith("GETALL"):
                            response = self.handle_getall()
                        elif data.startswith("GET:"):
                            name = data.split(":")[1]
                            response = self.handle_get(name)
                        else:
                            response = "ERROR: Invalid command"
                        connection.send(response.encode('utf-8'))
                    except BrokenPipeError:
                        self._logger.error("Broken pipe error - client may have disconnected.")
                        break  # Exit the loop if client has disconnected
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def handle_get(self, name):
        """Handle GET request to retrieve a specific entry"""
        return f"{name}:{self.directory.get(name, 'NOT FOUND')}"

    def handle_getall(self):
        """Handle GETALL request to retrieve all entries"""
        if not self.directory:
            return "EMPTY"
        return ";".join(f"{name}:{number}" for name, number in self.directory.items())

class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def get(self, name):
        """Retrieve a specific entry by name"""
        self.sock.send(f"GET:{name}".encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        print(data)
        return data

    def get_all(self):
        """Retrieve all directory entries"""
        self.sock.send("GETALL".encode('utf-8'))
        data = self.sock.recv(1024).decode('utf-8')
        print(data)
        return data

    def close(self):
        """ Close socket """
        self.sock.close()
        self.logger.info("Client down.")