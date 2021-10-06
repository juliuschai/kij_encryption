import socket
import logging
import blowfish

server_address = ('localhost',10001)
BUFFER_SIZE = 64
key = b'iloveprogramming'


class connection:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((server_address))
        self.sock.listen()
        self.Connect()
    
    def Connect(self):
        while True:
            conn, addr  = self.sock.accept()
            with conn:
                logging.warning('Connected :',addr)
                self.Receive(conn)
                   
                self.sock.close()
                return
    
    def Send(self):
        return
    
    def Receive(self,conn):
        with open('Output.zip','wb') as file:
            while True:
                data = conn.recv(BUFFER_SIZE)
                # self.Command(data)
                if len(data) == 0:
                    return
                if len(data) == 64:
                    data = self.Decypher(data)
                file.write(data)
            
        return
    
    def Retrieve(self):
        return
    
    def Decypher(self,data):
        cipher = blowfish.Cipher(b'Key must be between 4 and 56 bytes long.')
        return b"".join(cipher.decrypt_ecb(data))
        
if __name__ == '__main__':
    con = connection()
        
    