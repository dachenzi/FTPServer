import socket
import os
import struct
import json
import sys
from lib.MixInClass import BaleMixIn,GetFileDict
from lib.Encryption import fileEncry,passwordEncry

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
            if self._auth():
                while True:
                    data = input('>>:').strip()
                    if data == 'exit':
                        sys.exit('Bye bye')
                    command = data.split(' ')[0]
                    if not command:continue
                    if hasattr(self,command):
                        func = getattr(self,command)
                        func(data)
                    else:
                        self.info(data)
            else:
                continue

    def _auth(self):

        # 接受菜单
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len)
        print(data.decode('utf-8'),end='')

        # 输入用户名
        username = input('Username:').strip()
        password = input('Password:').strip()
        password_md5 = passwordEncry(password)
        userinfo = {
            'username':username,
            'password':password_md5
        }
        userinfo_json = json.dumps(userinfo)

        # 发送登陆用户名密码
        header_len = self._struct(userinfo_json.encode('utf-8'))
        self.client.send(header_len)
        self.client.send(userinfo_json.encode('utf-8'))

        # 接受验证结果
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len).decode('utf-8')
        if data == 'True':
            print('Welcome [ {} ] Login'.format(userinfo.get('username')))
            return True
        else:
            user_input = input('Accounts or Password was Error,Retry? [y/n]')
            if user_input == 'y' or user_input == 'Y':
                return False
            else:
                print('Bye Bye')
                sys.exit()

    def info(self,command):
        '''
        Used for Send Execute Command to Server
        :param command: User input Command
        :return: None
        '''

        if sys.platform == 'win32':
            code = 'gbk'
        else:
            code = 'UTF-8'


        header_len = self._struct(command.encode(code))
        self.client.send(header_len)
        self.client.send(command.encode(code))
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len)
        print(data.decode(code))

    def put(self,data):
        '''
        Send File to Server
        :param data: User input Execute
        :return:
        '''

        # 发送put命令
        header_len = self._struct(data.encode('utf-8'))
        self.client.send(header_len)
        self.client.send(data.encode('utf-8'))

        # 发送文件属性信息
        _,filepath,*other = data.split()
        file_dic = self.getfileinfo(filepath)
        if not file_dic:
            return 'File is not exists'
        file_dic_json = json.dumps(file_dic)
        dic_header = self._struct(file_dic_json.encode('utf-8'))
        self.client.send(dic_header)
        self.client.send(file_dic_json.encode('utf-8'))

        # 发送文件
        with open(filepath,'r') as f:
            data = f.read()
        data_len = self._struct(data.encode('utf-8'))
        self.client.send(data_len)
        self.client.send(data.encode('utf-8'))

        # 接受结果
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        data = self.client.recv(data_len)
        print(data.decode('utf-8'))

    def get(self,data):
        '''
        Download file from Server
        :param data:  User input Command
        :return: None
        '''

        # 获取下载路径(默认存放在桌面)
        if len(data.split()) <= 2 :
            filepath = r'C:\Users\Administrator\Desktop'
        else:
            filepath = data.split()[2]

        # 发送get命令
        header_len = self._struct(data.encode('utf-8'))
        self.client.send(header_len)
        self.client.send(data.encode('utf-8'))

        # 获取文件属性信息
        dic_header = self.client.recv(4)
        data_len = struct.unpack('i', dic_header)[0]
        file_dic_json = self.client.recv(data_len)
        try:
            file_dic = json.loads(file_dic_json,encoding='utf-8')
        except:
            print(file_dic_json.decode('utf-8'))
            return
        old_filename = file_dic['filename']
        old_filemd5 = file_dic['filemd5']
        old_filesize = file_dic['filesize']

        # 接受文件
        data_header = self.client.recv(4)
        data_len = struct.unpack('i', data_header)[0]
        file_content = self.client.recv(data_len)

        # 判断存储目录
        if os.path.isdir(filepath):
            new_file = os.path.join(filepath, old_filename)
        else:
            new_file = filepath

        # 写文件
        with open(new_file,'w') as f:
            f.write(file_content.decode('utf-8'))

        # 检查文件
        new_filemd5 = fileEncry(new_file)
        new_filesize = os.path.getsize(new_file)

        if new_filesize == old_filesize and new_filemd5 == old_filemd5:
            info = '下载文件成功'
        else:
            info = '下载文件失败'

        print('{},路径:{}'.format(info,new_file))