import socket
import logging
import blowfish
from Crypto.PublicKey import RSA

server_address = ('localhost',10001)
BUFFER_SIZE = 64


class connection:
    def __init__(self):
        self.key = b''
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((server_address))
        self.sock.listen()
        self.Connect()
    
    def Connect(self):
        while True:
            conn, addr  = self.sock.accept()
            with conn:
                logging.warning('Connected :',addr)
                self.Retrieve(conn)
                self.sock.close()
                return
    
    def Send(self):
        return
    
    def ReceiveData(self,conn):
        with open('Output.zip','wb') as file:
            while True:
                data = conn.recv(BUFFER_SIZE)
                # self.Command(data)
                if len(data) == 0:
                    return self.Retrieve(conn)
                if len(data) == 64:
                    data = self.Decypher(data)
                file.write(data)
            
        return
    
    def Retrieve(self,conn):
        while True:
            data =  conn.recv(BUFFER_SIZE).decode()
            j = data.split(" ")
            try:
                command = j[0].strip()
                if(command == "key"):
                    return self.KeyRetriever(command[1].strip(),conn)
                elif(command == "data"):
                    return self.ReceiveData(conn)
                
            except IndexError:
                return "-Command Error"
            
    
    def KeyRetriever(self,key,conn):
        if self.key == b'':
            self.key = RSA.import_key(key)
            return self.Retrieve(conn)
        else:
            return self.key
        
    
    def Decypher(self,data):
        cipher = blowfish.Cipher()
        return b"".join(cipher.decrypt_ecb(data))
        
if __name__ == '__main__':
    con = connection()
        
    