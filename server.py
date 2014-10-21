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

d = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            inf_client = self.client_address
            ip = str(inf_client[0])
            puerto = str(inf_client[1])
            if line:
                if line [0:8] == "REGISTER":
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    d[ip] = puerto
                    print d
                else:
                    self.wfile.write("Hemos recibido tu peticion")
                    print "IP: " + ip + " Port: " + puerto
                    print "El cliente nos manda " + line + "\n"
            else: # elif not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
