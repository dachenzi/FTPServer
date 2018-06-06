from lib import FTPClientClass



if __name__ == '__main__':
    client = FTPClientClass.FTPClient('127.0.0.1',8080)
    client.run()