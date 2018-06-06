import socket
import struct
import json
from lib.MixInClass import BaleMixIn

class FTPClient(BaleMixIn):

    def __init__(self,ipaddr,port):
       self.ip = ipaddr
       self.port = port

    def run(self):
        '''
        Used for User Input
        :return: None
        '''

        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.ip,self.port))
        while True:
            command = input('>>:').split(' ')[0]
            if not command:break
            if command == 'put':
                filenames = input('>>:').split(' ')[1]
                self.put(filenames)
            elif command == 'get':
                filenames = input('>>:').split(' ')[1]
                self.get(filenames)
            else:
                self.info(command)

    def info(self,command):
        '''
        Used for Send Execute Command to Server
        :param command: User input Command
        :return: None
        '''

        header_len = self._struct(command)
        self.client.send(header_len)
        self.client.send(command.encode('gbk'))
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len)
        print(data.decode('gbk'))

    def put(self,file):
        pass

    def get(self,file):
        pass


