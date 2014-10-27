#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#PRÁCTICA 4 --- JAVIER MARTÍNEZ MOLINA
"""
Programa cliente que abre un socket a un servidor
Introducimos campos desde la linea de comandos y comprobamos que son correctos
"""
import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    REGISTER = sys.argv[3].upper()
    DIRECCION = sys.argv[4]
    EXPIRES = sys.argv[5]

except ValueError:
    print 'Usage: client.py ip puerto register sip_address expires_value'
    raise SystemExit

if REGISTER != "REGISTER":
    print 'Usage: client.py ip puerto register sip_address expires_value'
    raise SystemExit

LINE = REGISTER + " sip:" + DIRECCION + " SIP/2.0" + "\r\n"
LINE = LINE + "Expires: " + EXPIRES + "\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))
# envio de contenido
print "Enviando: " + LINE
my_socket.send(LINE)
#recibo mensaje del servidor
data = my_socket.recv(1024)
print 'Recibido -- ', data
print "Terminando socket..."
# Cerramos todo
my_socket.close()
print "Fin."
