#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# PRÁCTICA 4 --- JAVIER MARTÍNEZ MOLINA

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Clase de un servidor SIP register
    """
    dic_reg = {}

    def register2file(self):
        """
        Cada vez que un user se registre o se dé de baja,
        se imprime en el fich una linea con los campos indicados
        y en sucesivas líneas los valores de cada user registrado.
        """
        fich = open("registered.txt", "w")
        fich.write("User\t" + "IP\t" + "Expires\r\n")
        for mail in self.dic_reg:
            segundos = self.dic_reg[mail][1]
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(segundos))
            fich.write(mail + "\t" + self.dic_reg[mail][0] + "\t" + t + "\r\n")
        fich.close()

    def handle(self):
        """
        Se comprueba que el tipo de mensaje es un REGISTER,
        la caducidad de los user, se añade al dic a los user
        que cumplen las condiciones y se borra a los user con EXPIRES a 0.
        """
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":
                list_palabras = line.split()
                if list_palabras[0] == "REGISTER":
                    #Compruebo mi dic para localizar posibles users EXPIRES
                    if self.dic_reg:
                        tiempo_actual = time.time()
                        for user in self.dic_reg.keys():
                            if self.dic_reg[user][1] <= tiempo_actual:
                                del self.dic_reg[user]
                        self.register2file()
                    #añado al user a la lista
                    time_expired = time.time() + float(list_palabras[4])
                    recorte = list_palabras[1].split(":")
                    mail = recorte[1]
                    self.wfile.write("SIP/2.0 200 OK\r\n")
                    list_atributos = [self.client_address[0], time_expired]
                    self.dic_reg[mail] = list_atributos
                    self.register2file()
                    #compruebo si el campos EXPIRES es 0
                    if int(list_palabras[4]) == 0:
                        del self.dic_reg[mail]
                        self.register2file()
                    print self.client_address
                    print line
                else:
                    self.wfile.write("SIP/2.0 400 Bad Request\r\n")
            if not line:
                break

if __name__ == "__main__":

    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco...\n"
    serv.serve_forever()
