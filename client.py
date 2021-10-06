from ctypes import sizeof
from os import SEEK_CUR, read, sched_setscheduler
import os
import socket
import base64
import blowfish
from Crypto.PublicKey import RSA

class connection:
    def __init__(self):
        self.ADDRESS = 'localhost'
        self.PORT = 10001
        BUFFER_SIZE = 1024
        self.key = b''
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Connect()
        
    def Connect(self):
        self.sock.connect((self.ADDRESS,self.PORT))
        self.SendFile()
        
    def Send(self,message):
        with open('/home/feinard/Documents/GitHub/AES-Implementation/civic_renewal_forms.zip','rb') as infile:
            while True:
                chunk_data = infile.read(64)
                if(len(chunk_data) == 0):
                    break
                elif len(chunk_data) == 64:
                    chunk_data = self.Encryptor(chunk_data)
                self.sock.SendFileall(chunk_data)
            infile.close()
        self.Command()
    
    def SendFile(self):
        return self.sock.sendall(message.encode())
    
    def Receive(self):
        return
    
    def KeyGenerator(self):
        if self.key == b'':
            self.key = RSA.generate(40)
            message = "key {}" . format(self.key)
            self.Send(message)

        return key
    
    def Encryptor(self,data):
        cipher = blowfish.Cipher(bytes(self.key, 'utf-8'))
        return b"".join(cipher.encrypt_ecb(data))
    
    def Command(self):
        while True:
            return
        
    
if __name__ == '__main__':
    connect = connection()
    
    