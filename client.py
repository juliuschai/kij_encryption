from ctypes import sizeof
from os import read, sched_setscheduler
import os
import socket
import base64
import blowfish

ADDRESS = 'localhost'
PORT = 10001
BUFFER_SIZE = 1024
key = '0123456789abcdef'

class connection:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Connect()
        
    def Connect(self):
        self.sock.connect((ADDRESS,PORT))
        self.Send()
    
    def Send(self):
        with open('/home/feinard/Documents/GitHub/AES-Implementation/civic_renewal_forms.zip','rb') as infile:
            while True:
                chunk_data = infile.read(64)
                if(len(chunk_data) == 0):
                    break
                elif len(chunk_data) == 64:
                    chunk_data = self.Encryptor(chunk_data)
                self.sock.sendall(chunk_data)
            infile.close()
        self.Command()
    
    def Receive(self):
        return
    
    def Encryptor(self,data):
        cipher = blowfish.Cipher(b'Key must be between 4 and 56 bytes long.')
        return b"".join(cipher.encrypt_ecb(data))
    
    def Command(self):
        while True:
            return
        
    
if __name__ == '__main__':
    connect = connection()
    
    