# coding: utf-8
__author__ = "wolf"

"""
文件接受端
"""


import socket
import threading

import sys
import os
import struct


def socket_build():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip=get_host_ip()
        ip_port = (ip, 9911)
        s.bind(ip_port)
        print('root:已建立对'+str(ip_port)+'的监听!')
        s.listen(10)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print ('root:等待通道建立请求...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print ('root:接收到一个来自 {0} 的请求！'.format(addr))
    #conn.settimeout(500)
    conn.send('root:TCP Socket for {0} build success !'.format(addr).encode())

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn =  filename.decode().strip('\00' )
            new_filename = os.path.join('./', 'copyNew_' + fn)
            print ('root：文件名：{0}, 文件大小： {1}Mb'.format(str(new_filename), round(int(filesize)/1024/1024,2) ))

            recvd_size = 1024  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print ('root:文件开始接收...')
            print ('root:接受进度 ', end=''),
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                    print ('#',end='')
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                    print ('# 【100%】')
                fp.write(data)
            fp.close()
            print ('root:文件接收完毕...')
        conn.close()
        break

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.1.1.1', 8880))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

if __name__ == '__main__':
    socket_build()
