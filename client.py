#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

line = ""
try:
    # puerto y servidor.
    server = str(sys.argv[1])
    port = int(sys.argv[2])
    # contenido a enviar.
    if sys.argv[3] == "register":
        line = "REGISTER" + " sip:" + sys.argv[4] + " SIP/2.0\r\n"
        line = line + "Expires: " + sys.argv[5] + "\r\n\r\n"
    else:
        for i in sys.argv[3:]:
            line = line + str(i) + str(" ")
except ValueError:
    print "Usage: client.py ip puerto register sip_address expires_value"
    sys.exit()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((server, port))

print "Enviando: " + line
my_socket.send(line + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
