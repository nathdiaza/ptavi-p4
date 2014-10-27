#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
# Cliente UDP simple.

# Dirección IP del servidor.

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METHOD = sys.argv[3]
    SIP_ADDRES = sys.argv[4]
    EXPIRES_VALUE = sys.argv[5]


    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    if METHOD == "register":
	    my_socket.send("REGISTER sip: " + SIP_ADDRES + " SIP/2.0" + '\r\n'+ "Expires: " + EXPIRES_VALUE + '\r\n\r\n')
	    data = my_socket.recv(1024)
	    print  data   
    my_socket.close()

	    
except (IndexError, ValueError):
   print "Usage: client.py ip puerto register sip_address expires_value"
# Cerramos todo
    
