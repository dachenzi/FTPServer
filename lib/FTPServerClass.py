import socketserver
import struct
import json
import subprocess
import os
import time
from lib.MixInClass import BaleMixIn,GetFileDict
from lib.Encryption import fileEncry
from lib import UserCheck


class FTPProcess(socketserver.BaseRequestHandler,BaleMixIn,GetFileDict):

    def handle(self):
        '''
        Handling user requests
        :return: None
        '''
        print('client\'s Address: {0}'.format(self.client_address))
        while True:  # 认证循环
            try :
                if self._Authorization():
                    while True:    # 通信循环
                        data_header = self.request.recv(4)
                        if not data_header:break
                        data_len = struct.unpack('i',data_header)[0]
                        data_bytes = self.request.recv(data_len)
                        data = data_bytes.decode('utf-8')
                        command = data.split(' ')[0]
                        print(data)
                        if hasattr(self,command):
                            func = getattr(self,command)
                            func(data)
                        else:
                            self.info(data)
                else:
                    continue
            except:
                break

    def _Authorization(self):

        '''
        Account Authorization
        :return: Authorization Result
        '''

        data = '''
---------> FTP Server Login Authorization <----------
time: {0}
'''.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        # 发送登陆认证菜单
        header_len = self._struct(data.encode('utf-8'))
        self.request.send(header_len)
        self.request.send(data.encode('utf-8'))

        # 接受用户名密码
        userinfo_header = self.request.recv(4)
        userinfo_len = struct.unpack('i', userinfo_header)[0]
        userinfo_json = self.request.recv(userinfo_len)
        userinfo = json.loads(userinfo_json,encoding='utf-8')

        # 验证用户密码
        if UserCheck.checkUser(userinfo.get('username'),userinfo.get('password')):
            data = 'True'
            header_len = self._struct(data.encode('utf-8'))
            self.request.send(header_len)
            self.request.send(data.encode('utf-8'))
            print('{} Login at {}'.format(userinfo.get('username'),time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            return True
        else:
            data = 'False'
            header_len = self._struct(data.encode('utf-8'))
            self.request.send(header_len)
            self.request.send(data.encode('utf-8'))
            return False

    def info(self,data):
        '''
        Used for Execute Command
        :param command: User input Command
        :return: Command stdout/stderr info
        '''

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

    def put(self,data):
        '''
        client Upload file
        :param data: User input command
        :return: none
        '''

        # 获取文件属性信息
        dic_header = self.request.recv(4)
        data_len = struct.unpack('i', dic_header)[0]
        file_dic_json = self.request.recv(data_len)
        file_dic = json.loads(file_dic_json,encoding='utf-8')
        old_filename = file_dic['filename']
        old_filemd5 = file_dic['filemd5']
        old_filesize = file_dic['filesize']

        # 判断目标是路径还是具体的文件
        *other,file_path = data.split()[:3]
        if not os.path.isdir(file_path):
            filepath = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
        else:
            filepath = file_path

        # 接受文件
        data_header = self.request.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        file_content = self.request.recv(data_len)
        new_file = os.path.join(filepath,filename)
        with open(new_file,'w') as f:
            f.write(file_content.decode('utf-8'))

        # 检查文件
        new_filemd5 = fileEncry(new_file)
        new_filesize = os.path.getsize(new_file)

        if new_filesize == old_filesize and new_filemd5 == old_filemd5:
            info = '上传文件成功'
        else:
            info = '上传文件失败'

        # 发送上传结果
        header_len = self._struct(info.encode('utf-8'))
        self.request.send(header_len)
        self.request.send(info.encode('utf-8'))

    def get(self,data):
        '''
        client download files
        :param data: User input command
        :return: none
        '''

        # 判断下载的文件是否存在
        *other, file_path = data.split()[:2]
        if not os.path.isfile(file_path):
            info = '文件不存在,请重新输入'
            header_len = self._struct(info.encode('utf-8'))
            self.request.send(header_len)
            self.request.send(info.encode('utf-8'))
            return

        # 发送文件信息
        file_dic = self.getfileinfo(file_path)
        file_dic_json = json.dumps(file_dic)
        dic_header = self._struct(file_dic_json.encode('utf-8'))
        self.request.send(dic_header)
        self.request.send(file_dic_json.encode('utf-8'))

        # 发送文件
        with open(file_path,'r') as f:
            data = f.read()
        data_len = self._struct(data.encode('utf-8'))
        self.request.send(data_len)
        self.request.send(data.encode('utf-8'))



class FTPServer(object):

    def __init__(self,ipaddr,port):
        self.ipaddr = ipaddr
        self.port = port

    def run(self):
        server = socketserver.ThreadingTCPServer((self.ipaddr,self.port), FTPProcess)
        server.serve_forever()

