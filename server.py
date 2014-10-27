#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    dic_registro = {}
    
    def register2file(self):
        fich = open("registered.txt", "w")
        fich.write("User\t\t\t\t" + "IP\t\t\t" + "Expires\r\n")
        for mail in self.dic_registro:
            tiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.dic_registro[mail][1]))
            fich.write(mail +"\t" + self.dic_registro[mail][0] + "\t" + tiempo +"\r\n")
        fich.close()
       
    def handle(self):
    
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":
                list_palabras = line.split()
                if list_palabras[0] == "REGISTER":
                    #Compruebo mi diccionario para localizar posibles users EXPIRES
                    if self.dic_registro:
                        tiempo_actual = time.time()
                        for user in self.dic_registro.keys():
                            if self.dic_registro[user][1] <= tiempo_actual:
                                del self.dic_registro[user]
                        self.register2file()
                    #añado al user a la lista
                    time_expired = time.time() + float(list_palabras[4])
                    recorte = list_palabras[1].split(":")
                    mail = recorte[1]
                    self.wfile.write("SIP/2.0 200 OK\r\n")
                    list_atributos = [self.client_address[0], time_expired]
                    self.dic_registro[mail] = list_atributos
                    self.register2file()
                    #compruebo si el campos EXPIRES es 0
                    if int(list_palabras[4]) == 0:
                        del self.dic_registro[mail]
                        self.register2file()
                print self.client_address
                print line
            if not line:
                break

if __name__ == "__main__":

    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco...\n"
    serv.serve_forever()
