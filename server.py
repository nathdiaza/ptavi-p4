#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    dic_registro = {}
    fich = open("registered.txt", "a")
    fich.write("User\t" + "IP\t" + "Expires\n")
    fich.close()
    
    def register2file(self, usuario, ip, tiempo):

        fich = open("registered.txt", "a")
        fich.write(usuario +"\t" + ip + "\t" + tiempo +"\n")
        fich.close()


    def handle(self):
    
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":
                list_palabras = line.split()
            if list_palabras[0] == "REGISTER":
                recorte = list_palabras[1].split(":")
                mail = recorte[1]
                self.wfile.write("SIP/2.0 200 OK\r\n")
                tiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                self.register2file(mail, self.client_address[0], tiempo)
                self.dic_registro[mail] = self.client_address[0]
                print self.dic_registro
                if int(list_palabras[4]) == 0:
                    del self.dic_registro[mail]
                    print self.dic_registro
            print self.client_address
            print line
            if not line:
                break

if __name__ == "__main__":

    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco...\n"
    serv.serve_forever()
