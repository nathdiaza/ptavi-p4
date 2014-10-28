#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de SIP
en UDP simple
"""

import SocketServer
import sys
import time

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    List_Client = {}
    def handle(self):
    
    	for client in List_Client.keys():
    	
		if List_Client[client][1]< time.time():
			del List_Client[client]
			print "Expira: " + str(client) + "\r"
			# Imprimir sólo si no está vacío
			if List_Client:
				print List_Client
		
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente manda: " + line
            line = line.split()
            if "REGISTER" in line:
     		if line[5] == "0":
     			if line[2] in List_Client:
     				del List_Client[line[2]]
     				print "Borramos a: " + str(line[2]) + "\r"
     		else :
            		List_Client[line[2]] = (self.client_address[0],time.time()+float(line[5]))
            		print "Entra: " + str(line[2]) + "\r"
            	self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            	self.register2file()	
            else:
            	self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n"
            if not line:
                break
                
                
    def register2file(self):
    
    	fich = open("registered.txt", 'w')
    	line = ("Use"+ "\t" + "IP" + "\t" + "Expires"+ "\r\n")
    	for client in List_Client.keys():
    		h_Expires = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(List_Client[client][1]))
    		line += x + "\t" + List_Client[client][0] + "\t" + h_Expires + "\r\n"
	fich.write(line)    
    	fich.close()

if __name__ == "__main__":
    # Creamos servidor de SIP y escuchamos
    serv = SocketServer.UDPServer(("",int(sys.argv[1])), SIPRegisterHandler)
    print "\nLanzando servidor UDP de SIP... \r\n"
    serv.serve_forever()
