#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de sip
en UDP simple
"""

import SocketServer
import sys

diccionario = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """

    def handle(self):
        # Tomo dirección y puerto del cliente (de tupla client_address)
        ip_port = self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break

            print "El cliente nos manda " + line

            # Mientras que la línea no esté vacía
            lista = line.split()
            print "lista: " + str(lista) + "\r"
            metodo = lista[0]
            print "metodo: " + str(metodo) + "\r"

            if metodo == "REGISTER":
                direc = lista[1].split(":")[1]
                print "direccion: " + str(direc) + "\r"
                expires = int(lista[4])
                print "expires: " + str(expires) + "\r"
                
                if expires > 0: 
                    if not direc in diccionario:
                        print "entra en el diccionario: " + str(direc) + "\r"  
                    diccionario[direc] = ip_port[0]
                    print "diccionario: " + str(diccionario) + "\r"   
                else:
                    if direc in diccionario:
                        del diccionario[direc] 
                        print "borro del diccionario a: " + str(direc) + "\r"  
                        if diccionario:   
                            print "diccionario: " + str(diccionario) + "\r"                      
                    
                respuesta = "SIP/2.0 200 OK \r\n\r\n"
            else:
                respuesta = "SIP/2.0 400 Bad Request \r\n\r\n"
                
            print "\r\nRespondo al cliente: " + respuesta
            self.wfile.write(respuesta)

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "\nLanzando servidor UDP de SIP... \r\n"
    serv.serve_forever()
