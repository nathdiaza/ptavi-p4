#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


PORT = int(sys.argv[1])
dic_clients = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print "El cliente nos manda " + line
            EMAIL = line.split()[1][4:]
            IP = self.client_address[0]
            print "Guardamos EMAIL: " + EMAIL + " y la IP: " + IP
            dic_clients[EMAIL] = IP


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
