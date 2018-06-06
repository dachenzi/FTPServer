import socketserver
import struct
import json
import subprocess
from lib.MixInClass import BaleMixIn


class FTPProcess(socketserver.BaseRequestHandler,BaleMixIn):

    def handle(self):
        print('client\'s Address: {0}'.format(self.client_address))
        while True:
            data_header = self.request.recv(4)
            if not data_header:break
            data_len = struct.unpack('i',data_header)[0]
            data_bytes = self.request.recv(data_len)
            data = data_bytes.decode('utf-8')
            command = data.split(' ')[0]
            if command == 'put':
                filenames = data.split(' ')[1]
                self.put(filenames)
            elif command == 'get':
                filenames = data.split(' ')[1]
                self.get(filenames)
            else:
                self.info(data)

    def put(self,file):
        pass

    def get(self,file):
        pass

    def info(self,data):
        '''
        Used for Execute Command
        :param command: User input Command
        :return: Command stdout/stderr info
        '''
        print(data.split())
        command = subprocess.Popen(data.split(),
                                   shell=True,
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        err = command.stderr.read()
        if not err:
            info = command.stdout.read()
            header_len = self._struct(info)
            self.request.send(header_len)
            self.request.send(info)
        else:
            header_len = self._struct(err)
            self.request.send(header_len)
            self.request.send(err)

class FTPServer(object):

    def __init__(self,ipaddr,port):
        self.ip = ipaddr
        self.port = port

    def run(self):
        server = socketserver.ThreadingTCPServer((self.ip,self.port), FTPProcess)
        server.serve_forever()

