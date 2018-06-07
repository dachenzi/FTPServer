import sys
from os.path import abspath, dirname
sys.path.insert(0, abspath(dirname(dirname(__file__))))
from lib import  FTPServerClass
import configparser
import os
import getpass
from conf import settings
from lib import Encryption

def getConfig():
    '''
    read parser from Config Files
    :return: parser Dictionary
    '''

    cp = configparser.ConfigParser(allow_no_value=True)
    configFiles = os.path.join(os.path.dirname(os.path.dirname(__file__)),settings.CONFIG_FILES)
    dbFiles = os.path.join(os.path.dirname(os.path.dirname(__file__)),settings.DB_FILES)
    cp.read(configFiles)
    config_dic = {
        'dbFiles':dbFiles,
        'FTPserver':cp['TCPServer'].get('IPADDR'),
        'FTPport':int(cp['TCPServer'].get('PORT'))
    }

    return config_dic


def checkUser(input_user,input_password):
    '''
    check user Account Information
    :param input_user: User input UserName
    :param input_password: User input Password
    :return: Authentication results
    '''

    pass_file = getConfig().get('dbFiles')
    with open(pass_file,'r') as f:
        for line in f:
            user,password = line.strip().split(',')
            if user == input_user and password == input_password:
                return True
    return False

if __name__ == '__main__':

    print('-------> Run FTP Server <---------')
    while True:
        username = input('Username:')
        password = input('Password:')
        # password = getpass.getpass('Password:')    # 密文,windows 10 下测试会卡住
        password_md5 = Encryption.passwordEncry(password)
        if checkUser(username,password_md5):
            config_dic = getConfig()
            ftp = FTPServerClass.FTPServer(config_dic.get('FTPserver'),config_dic.get('FTPport'))
            print('启动FTP Server服务,开始等待链接')
            ftp.run()
        else:
            user_input = input('账号或者密码错误,是否请重试 (y/n): ')
            if user_input == 'y' or user_input == 'Y':
                continue
            else:
                print('Bye Bye')
                break