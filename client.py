from ctypes import sizeof
from os import EX_PROTOCOL
import socket
from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import Blowfish, PKCS1_OAEP

class connection:
    def __init__(self):
        self.ADDRESS = 'localhost'
        self.PORT = 10000
        self.BUFFER_SIZE = 2048
        self.key = b''
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Connect()
        
    def Connect(self):
        print("Connecting........")
        self.sock.connect((self.ADDRESS,self.PORT))
        
        print("Connect Success!")
        self.Command()
        
    def Send(self,message):
        return self.sock.sendall(message.encode())
       
    
    def SendFile(self):
        print("Sending File.........")
        self.Send('data')
        with open('civic_renewal_forms.zip','rb') as infile:
            while True:
                chunk_data = infile.read(64)
                if(len(chunk_data) == 0):
                    break
                elif len(chunk_data) == 64:
                    chunk_data = self.Encryptor(chunk_data)
                self.sock.send(chunk_data)
            infile.close()
        self.Command()
    
    def RSARetrivever(self,RSAvalue):
        self.private_key =  RSA.import_key(RSAvalue)
        self.private_key = PKCS1_OAEP.new(self.private_key)
        return self.Command()
    
    def keyRetriever(self):
        key = self.sock.recv(self.BUFFER_SIZE)
        self.key = self.private_key.decrypt(key)
        return self.SendFile()
    
    def Encryptor(self,data):
        Cipher = Blowfish.new(self.key,Blowfish.MODE_ECB)
        return b"".join(Cipher.encrypt(data))
    
    def Command(self):
        while True:
            data =  self.sock.recv(self.BUFFER_SIZE)
            data = data.decode()
            j = data.split('\r\n\r\n')
            command = j[0].strip()
            if(command == "RSA"):
                print("Getting RSA.........")
                self.RSARetrivever(j[1])
                print("RSA Receive.........")
            if command == "key":
                print("Getting Key.........")
                self.keyRetriever()
                print("Key Receive.........")
            return
        
    
if __name__ == '__main__':
    connect = connection()
    
    
    