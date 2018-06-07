import sys
from os.path import abspath, dirname
sys.path.insert(0, abspath(dirname(dirname(__file__))))
import getpass
from lib import FTPServerClass
from lib import UserCheck
from lib import Encryption


if __name__ == '__main__':

    print('-------> Run FTP Server <---------')
    while True:
        username = input('Username:')
        password = input('Password:')
        # password = getpass.getpass('Password:')    # 密文,windows 10 下测试会卡住
        password_md5 = Encryption.passwordEncry(password)
        if UserCheck.checkUser(username,password_md5):
            config_dic = UserCheck.getConfig()
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