#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de sip
en UDP simple
"""
import SocketServer
import sys
import time

diccionario = {}
formato_time = '%Y-%m-%d %H:%M:%S'


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    def handle(self):
        ip_port = self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print "El cliente nos manda: " + line
            lista = line.split()
            metodo = lista[0]

            # Si el método es correcto: REGISTER
            if metodo == "REGISTER":

                # Primero vemos si alguien ha expirado
                self.ver_si_expire()

                # Cliente nuevo según su expire
                direc = lista[1].split(":")[1]
                expires = int(lista[4])
                if expires > 0:
                    if not direc in diccionario:
                        print "... entra en el dicc: " + str(direc) + "\r"
                    else:
                        print "... modifico del dicc: " + str(direc) + "\r"
                    time_exp = time.gmtime(time.time() + expires)
                    day_time_exp = time.strftime(formato_time, time_exp)
                    diccionario[direc] = [ip_port[0], day_time_exp]
                    print "diccionario: " + str(diccionario) + "\r"
                else:
                    if direc in diccionario:
                        del diccionario[direc]
                        print "... borro del dicc a: " + str(direc) + "\r"
                        if diccionario:
                            print "diccionario: " + str(diccionario) + "\r"
                self.register2file()
                respuesta = "SIP/2.0 200 OK \r\n\r\n"

            else:
                respuesta = "SIP/2.0 400 Bad Request \r\n\r\n"

            print "\r\n\r\nRespondo al cliente: " + respuesta
            self.wfile.write(respuesta)

    """
    Fichero registered.txt class
    """
    def register2file(self):
        fich = open("registered.txt", 'w')
        fich.write("User\tIP\tExpires\r\n")
        for direc in diccionario.keys():
            IP = str(diccionario[direc][0])
            expires = str(diccionario[direc][1])
            fich.write(direc + "\t" + IP + "\t" + expires + "\r\n")
        fich.close()

    """
    Ver si alguien del diccionario ha expirado
    """
    def ver_si_expire(self):
        for direc in diccionario.keys():
            expires = str(diccionario[direc][1])
            time_now = time.gmtime(time.time())
            day_time_now = time.strftime(formato_time, time_now)
            if expires <= day_time_now:
                del diccionario[direc]
                print "... expira del dicc: " + str(direc) + "\r"
                if diccionario:
                    print "diccionario: " + str(diccionario) + "\r"

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    # Creamos servidor de sip y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "\nLanzando servidor UDP de SIP... \r\n"
    serv.serve_forever()
