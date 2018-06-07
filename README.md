# FTPServer
`使Python3 配合 socketserver 模块，模拟FTP服务器，主要用来练习`
### 目录结构
* bin：可执行命令（包含客户端，服务端）
* conf：socketserver的配置文件
* db：用户认证文件
* lib：依赖的库和类文件
### 支持的命令
* **get**：用于下载文件
```ruby
get D:\PythonScript\hello.py D:\PythonScript\linux.py
get D:\PythonScript\hello.py (默认存储在桌面)
```
* **put**: 用于上传文件
```ruby
put D:\PythonScript\hello.py D:\PythonScript\linux.py
```
* **command**: 用于执行普通命令
### 启动服务端
```shell
cd FTPServer
python3 bin/server.py
```
### 启动客户端
```shell
cd FTPServer
python3 bin/client.py
```
