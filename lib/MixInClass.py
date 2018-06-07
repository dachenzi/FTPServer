import struct
import os
from lib import Encryption

class BaleMixIn(object):

    def _struct(self ,data):
        '''
        compute Package header
        :param data: User transport Data
        :return: Package header
        '''
        data_header = struct.pack('i' ,len(data))
        return data_header

class GetFileDict(object):

    def getfileinfo(self,filename):

        if not os.path.exists(filename):
            return False

        file_name = os.path.basename(filename)
        file_md5 = Encryption.fileEncry(filename)
        file_size = os.path.getsize(filename)

        file_dict = {
            'filename':file_name,
            'filemd5':file_md5,
            'filesize':file_size
        }
        return  file_dict