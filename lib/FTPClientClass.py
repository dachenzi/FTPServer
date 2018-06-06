import socket
import struct
import json
from lib.MixInClass import BaleMixIn,GetFileDict
from lib.Encryption import fileEncry

class FTPClient(BaleMixIn,GetFileDict):

    def __init__(self,ipaddr,port):
       self.ipaddr = ipaddr
       self.port = port

    def run(self):
        '''
        Used for User Input
        :return: None
        '''

        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.ipaddr,self.port))
        while True:
            data = input('>>:').strip()
            command = data.split(' ')[0]
            if not command:continue
            if hasattr(self,command):
                func = getattr(self,command)
                func(data)
            else:
                self.info(data)

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

    def put(self,data):

        # 发送put命令
        header_len = self._struct(data)
        self.client.send(header_len)
        self.client.send(data.encode('gbk'))

        # 发送文件属性信息
        _,filepath,*other = data.split()
        file_dic = self.getfileinfo(filepath)
        print(file_dic)
        if not file_dic:
            return 'File is not exists'
        file_dic_json = json.dumps(file_dic)
        dic_header = self._struct(file_dic_json)
        self.client.send(dic_header)
        self.client.send(file_dic_json.encode('utf-8'))

        # 发送文件
        with open(filepath,'r') as f:
            data = f.read()
        data_len = self._struct(data)
        self.client.send(data_len)
        self.client.send(data.encode('gbk'))

        # 接受结果
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len)
        print(data.decode('utf-8'))

    def get(self,data):
        pass


