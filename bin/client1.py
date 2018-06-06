from socket import *

host ='127.0.0.1'	#我是本机操作，所以host写localhost，如果是连接外部的服务器，host就要等于服务器的ip地址
port = 8080
bufsize = 1024
addr = (host,port)
client = socket(AF_INET,SOCK_STREAM)
client.connect(addr)
while True:
    data = input('>>: ')
    if not data or data=='exit':
        break
    client.send(data.encode('utf-8'))
    data = client.recv(bufsize)
    if not data:
        break
    print (data.decode('utf-8'))
client.close()