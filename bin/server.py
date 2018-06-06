from lib import  FTPServerClass



if __name__ == '__main__':
    ftp = FTPServerClass.FTPServer('127.0.0.1',8080)
    ftp.run()

