#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de SIP
en UDP simple
"""

import SocketServer
import sys
import time
import os

try:
    # puerto y servidor.
    PORT = int(sys.argv[1])
except ValueError:
    print "Error: los parametros pasados son erroneos"
    sys.exit()

dicc = {}


def register2file():
    deletekey = ""
    fichero1 = open("registered.txt", "w")
    fichero1.write("User\tIP\tExpires\n")
    for key in dicc:
        fichero1.write(key + "\t" + dicc[key][0] + "\t" + dicc[key][1] + "\n")
    fichero1.close
    fichero1 = open("registered.txt", "r")
    linea = fichero1.readline()
    for key in dicc:
        linea = fichero1.readline()
        hora = linea.split("\t")[2].split("\n")[0]
        horafrmt = time.mktime(time.strptime(hora, "%y/%m/%d %H:%M:%S")) + 3600
        if horafrmt < time.time():
            deletekey = key
    if not deletekey == "":
        del dicc[deletekey]
    fichero1.close
    fichero2 = open("registered.txt", "w")
    fichero2.write("User\tIP\tExpires\n")
    for key in dicc:
        fichero2.write(key + "\t" + dicc[key][0] + "\t" + dicc[key][1] + "\n")
    fichero2.close


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda: " + line
            # Escribe dirección y puerto del cliente (de tupla client_address)
            inf_client = self.client_address
            ip = str(inf_client[0])
            puerto = str(inf_client[1])
            if line:
                if line[0:8] == "REGISTER":
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    direccion = line.split(":")[1].split(" ")[0]
                    expires = line.split(":")[2].split(" ")[1]
                    hora = time.gmtime(time.time() + int(expires))
                    horaformato = time.strftime("%y/%m/%d %H:%M:%S", hora)
                    dicc[direccion] = (ip, horaformato)
                    print "entra: " +  str(direccion) + "\r"
                    if int(expires) == 0:
                        del dicc[direccion]
                        print "borro a: " +  str(direccion) + "\r"
                    register2file()

                else:
                    self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n")
            else:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de SIP..."
    serv.serve_forever()
