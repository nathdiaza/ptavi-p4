#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

LINE = ""
try:
    # puerto y servidor.
    SERVER = str(sys.argv[1])
    PORT = int(sys.argv[2])
    # contenido a enviar.
    if sys.argv[3] == "register":
        LINE = "REGISTER" + " sip:" + sys.argv[4] + " SIP/2.0\r\n"
        LINE = LINE + "Expires: " + sys.argv[5] + "\r\n\r\n"
    else:
        for i in sys.argv[3:]:
            LINE = LINE + str(i) + str(" ")
except ValueError:
    print "Usage: client.py ip puerto register sip_address expires_value"
    sys.exit()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
