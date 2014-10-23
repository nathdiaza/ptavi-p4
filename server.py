#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print line
            line = line.split()
            if "REGISTER" in line:
            	print self.client_address
            	self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("",int(sys.argv[1]) ), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
