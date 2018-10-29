#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    
    dicc_usuario = {}
    
    def handle(self):
       
        info_usuarios = {}
        
        IP = self.client_address[0]
        print("IP cliente: ", IP)
        PORT = self.client_address[1]
        print("Puerto: ", str(PORT))
        
        line = self.rfile.read()

        info = line.decode('utf-8')
        
        if (len(info) >= 2):
            if (info.split()[0].upper() == "REGISTER"):
                self.json2registered()
                direccion = info.split()[1]
                expiracion = int(info.split()[2])
                expires = int(time.time()) + expiracion
                tiempo_expiracion = time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.gmtime(expires))
                info_usuarios["direccion"] = self.client_address[0]
                info_usuarios["expires"] = tiempo_expiracion
                
                if (expiracion == 0):
                    if(len(self.dicc_usuario) != 0):
                        del self.dicc_usuario[direccion]
                elif ("@"in direccion):
                    self.dicc_usuario[direccion] = info_usuarios
                print(self.dicc_usuario)
                #json
                for usuario in dicc_usuario:
                    tiempo = time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.gmtime(time.time()))
                    atrib = self.dicc_usuario[usuario]
                    valor = atrib["expires"]
                    if (str(tiempo) > valor):
                        del self.dicc_usuario[direccion]             
                        
                        
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                  
                  
    def register2json(self):
        file_json = json.dumps(self.dicc_usuario)
        with open("registered.json", "w") as file_json:
            json.dump(self.dicc_usuario, file_json, sort_keys=True, indent=4)

if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
