# coding: utf-8
__author__ = "wolf"

"""
文件发送端
"""

import socket
import os
import sys
import struct
import re

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            IP = input("请求建立socket通道ip地址为：")
            if check_Ip(IP):
                break
        ip_port = (IP, 9911)
        s.connect(ip_port)
    except socket.error as msg:
        print (msg)
        sys.exit(1)

    print (s.recv(1024))

    while 1:
        filepath = input('root：输入文件路径: ')
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')), os.stat(filepath).st_size)
            s.send(fhead)
            #print ('root：文件路径: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('root:文件-{0} 传输完毕！'.format(filepath))
                    break
                s.send(data)
        s.close()
        break

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.1.1.1', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
#检验输入IP
def check_Ip(ip):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                ip):
        print ('root:当前输入 '+ip+'正则通过！')
        return True
    else:
        print ('root:当前输入 '+ip + '正则失败，重新输入！')
        return False

if __name__ == '__main__':
    socket_client()

