#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

try:
    # puerto y servidor.
    PORT = int(sys.argv[1])
except ValueError:
    print "Error: los parametros pasados son erroneos"
    sys.exit()

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            inf_client = self.client_address
            print "IP: " + str(inf_client[0]) + " Puerto: " + str(inf_client[1])
            print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
