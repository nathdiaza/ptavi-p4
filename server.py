#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            dic_registro = {}
            if line != "":
                list_palabras = line.split()
                recorte = list_palabras[1].split(":")
                mail = recorte[1]
                if list_palabras[0] == "REGISTER":
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    dic_registro[mail] = self.client_address[0]
                print self.client_address
                print line
            if not line:
                break

if __name__ == "__main__":

    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco...\n"
    serv.serve_forever()
