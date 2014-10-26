#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de SIP
en UDP simple
"""

import SocketServer
import sys
import time


PORT = int(sys.argv[1])
dic_clients = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server register class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break  
            print "El cliente nos manda: " + line
            #Cogemos los datos del cliente 
            user = line.split()[1][4:]
            ip = self.client_address[0]
            metodo = line.split('\r\n')[0][:8]
            exp = int(line.split('\r\n')[1][8:])
            
            if metodo == 'REGISTER':  
                hora_exp = time.time() + exp
                expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(hora_exp))     
                if exp == 0:
                    #Borramos al cliente del diccionario
                    del dic_clients[user]
                    print "Borramos a :" + user
                else:
                    print "Guardamos user: " + user + " y la IP: " + ip + '\n'
                    dic_clients[user] = ip
                    
                self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n') 
                self.register2file(user, ip, expires)
                
                print "DICCIONARIO CLIENTES:", dic_clients
                print

            print "Buscamos clientes"
            
            self.buscar_clientes(dic_clients)

    def register2file(self, user, ip, expires):
        """
        Registramos a los clientes en un fichero:
        """
        fich = open('registered', 'r+')
        linea = fich.readlines()
        if linea == []:
            fich.write('User' + '\t' + 'IP' + '\t' + 'Expires' + '\n')
        fich.write(user + '\t' + ip + '\t' + str(expires) + '\n')
        fich.close()

    def buscar_clientes(self, dic_clients):
        """
        Buscamos si ha caducado el expire de los clientes y en ese caso se borran
        """
        fich = open('registered', 'r')
        linea = fich.readlines()
        for cliente in linea:
            if len(cliente) != 16: #No es la primera linea
                expires = cliente.split(' ')[1]
                hora = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
                hora = hora.split(' ')[1]
                if expires == hora:
                    user = cliente.split(' ')[0]
                    print user
                    del dic_clients[user]
                    print "Borramos a :" + user
                    self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
        fich.close()
    
    
if __name__ == "__main__":
    # Creamos servidor register y escuchamos
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor register de SIP..." + '\n'
    serv.serve_forever()
