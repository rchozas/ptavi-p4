#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc_usuario = {}
    
    def handle(self):
        IP = self.client_address[0]
        print("IP cliente: ", IP)
        PORT = self.client_address[1]
        print("Puerto: ", str(PORT))
        
        line = self.rfile.read()

        info = line.decode('utf-8')
        
        if (len(info) >= 2):
            if (info.split()[0].upper() == "REGISTER"):
                self.dicc_usuario[info.split()[1]] = self.client_address[0]
                self.wfile.write(b"Hemos recibido tu peticion\r\n\r\n")
            elif (int(info.split()[2]) == 0):
                if(len(self.dicc_usuario) != 0):
                    del self.dicc_usuario[info.split()[1]]
            print(self.dicc_usuario)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
  
                  
        

if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
