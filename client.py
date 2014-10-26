#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


if len(sys.argv) != 6:
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit
    
# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
USER = sys.argv[4]
EXPIRES = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

#Creamos la petición de registro
LINE = "REGISTER" + " sip:" + USER + " SIP/2.0" + '\r\n'
#Creamos la cabecera
CABECERA = "Expires: " + EXPIRES + '\r\n\r\n'

LINE = LINE + CABECERA
print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
