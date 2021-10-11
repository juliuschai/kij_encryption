import socket
import logging
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import blowfish

BUFFER_SIZE = 64


class connection:
    def __init__(self):
        self.key = b''
        self.time = time.time()
        self.blowfish = blowfish.blowfish()
        self.server_address = ('localhost',10001)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen()
        self.Connect()
    
    def Connect(self):
        while True:
            self.conn, self.addr = self.sock.accept()
            with self.conn:
                logging.warning(f'Connected to {self.addr}')
                self.Command()
                self.sock.close()
                return
    
    def Send(self,command,message):
        message = b"\r\n\r\n".join([command.encode('utf-8'),message])
        return self.conn.sendall(message)
    
    def ReceiveData(self):
        print('Receiving Data')
        with open('buffer.txt','wb') as file:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                if data == b'':
                    file.close()
                    break
                file.write(data)
            file.close()

        with open('output.txt','w') as file:
            with (open('buffer.txt','rb')) as buffer_file:
                data = buffer_file.read()
                data = data.split(b'\r\n\r\n')
                for i in data:
                    if len(i.decode()) < 8 :
                        break
                    h = self.blowfish.decrypt(i.decode())
                    file.write(h)
                buffer_file.close()
            file.close()
            logging.warning(f"Time taken = {time.time() - self.time} seconds")
    
    def KeyGenerator(self):
        key = RSA.generate(2048)
        private_key = key.export_key('PEM')
        public_key = key.public_key().export_key('PEM')
        
        self.Send('RSA',private_key)
        
        self.key = "this is example text"
        self.blowfish.compute_with_key(self.key)
        self.key = self.key.encode()

        rsa_public_key = RSA.import_key(public_key)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        
        self.encrypt_key = rsa_public_key.encrypt(self.key)
        
        self.Send('key',self.encrypt_key)
        
        return
    
    def Decypher(self,data):
        return self.blowfish.decrypt(data)

    def Command(self):
        print("Sending RSA and Key.........")
        self.KeyGenerator()
        while True:
            data = self.conn.recv(BUFFER_SIZE).decode()
            j = data.split(" ")
            command = j[0].strip()
            if(command == "data"):
                return self.ReceiveData()
        
if __name__ == '__main__':
    con = connection()
        
    