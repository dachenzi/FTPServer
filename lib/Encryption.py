import hashlib
import os


def passwordEncry(password):
    '''
    Used for Password MD5 Encryption
    :param password:  User Input Password
    :return: MD5 string
    '''
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def fileEncry(file):
    '''
    compute file md5 code
    :param file:
    :return:
    '''
    if not os.path.exists(file):
        return False
    md5 = hashlib.md5()
    with open(file,'r') as f:
        for line in f:
            md5.update(line.encode('utf-8'))
    return md5.hexdigest()
