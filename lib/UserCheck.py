import configparser
import os
from conf import settings

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
