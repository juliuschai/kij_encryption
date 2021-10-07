from os import SEEK_CUR, wait
import socket
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Blowfish

server_address = ('localhost',10000)
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
            self.conn, self.addr  = self.sock.accept()
            with self.conn:
                logging.warning('Connected :',self.addr)
                self.Command()
                self.sock.close()
                return
    
    def Send(self,command,message):
        message = b"\r\n\r\n".join([command.encode('utf-8'),message])
        print(message)
        return self.conn.sendall(message)
    
    def ReceiveData(self):
        with open('Output.zip','wb') as file:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                # self.Command(data)
                if len(data) == 0:
                    return self.Retrieve(self.conn)
                if len(data) == 64:
                    data = self.Decypher(data)
                file.write(data)
    
    def Command(self):
        print("Sending RSA and Key.........")
        self.KeyGenerator()
        while True:
            data =  self.conn.recv(BUFFER_SIZE).decode()
            j = data.split(" ")
            command = j[0].strip()
            if(command == "data"):
                return self.ReceiveData(self.conn)
            
    
    def KeyGenerator(self):
        key = RSA.generate(2048)
        private_key = key.export_key('PEM')
        public_key = key.public_key().export_key('PEM')
        
        self.Send('RSA',private_key)
        
        self.key = str.encode("this is example text")
        
        
        rsa_public_key = RSA.import_key(public_key)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        
        self.encrypt_key = rsa_public_key.encrypt(self.key)
        
        self.Send('key',self.encrypt_key)
        
        return 
        
    
    def Decypher(self,data):
        cipher = Blowfish.new(self.key,Blowfish.MODE_ECB)
        return b"".join(cipher.decrypt(data))
        
if __name__ == '__main__':
    con = connection()
        
    