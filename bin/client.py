import sys
from os.path import abspath, dirname
sys.path.insert(0, abspath(dirname(dirname(__file__))))
from lib import FTPClientClass



if __name__ == '__main__':
    client = FTPClientClass.FTPClient('127.0.0.1',8080)
    client.run()