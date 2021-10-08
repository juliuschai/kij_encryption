import socket
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Blowfish

BUFFER_SIZE = 64


class connection:
    def __init__(self):
        self.key = b''
        self.server_address = ('localhost',10001)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
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
        return self.conn.sendall(message)
    
    def ReceiveData(self):
        with open('Output.zip','wb') as file:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                if data == b'\r\n\r\n' or data == b'':
                    file.close()
                    break
                elif len(data) >= 64:
                    data = self.Decypher(data)
                file.write(data)
            
            self.sock.close()
    
    def Command(self):
        print("Sending RSA and Key.........")
        self.KeyGenerator()
        while True:
            data =  self.conn.recv(BUFFER_SIZE).decode()
            j = data.split(" ")
            command = j[0].strip()
            if(command == "data"):
                return self.ReceiveData()
            
    
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
        return cipher.decrypt(data)
        
if __name__ == '__main__':
    con = connection()
        
    