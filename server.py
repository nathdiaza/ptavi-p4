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
                if int(list_palabras[4]) != 0:
                    if list_palabras[0] == "REGISTER":
                        recorte = list_palabras[1].split(":")
                        mail = recorte[1]
                        self.wfile.write("SIP/2.0 200 OK\r\n")
                        dic_registro[mail] = self.client_address[0]
                else:
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    recorte = list_palabras[1].split(":")
                    mail = recorte[1]
                    dic_registro[mail] = self.client_address[0]
                    del dic_registro[mail]
                print self.client_address
                print line
            if not line:
                break

if __name__ == "__main__":

    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco...\n"
    serv.serve_forever()
