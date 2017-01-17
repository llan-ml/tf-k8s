# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 09:51:16 2017
@author: DW
"""
#!/usr/bin/python
import socket
HOST='127.0.0.1'
PORT=50007

def request(request):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
        s.connect((HOST,PORT))       #要连接的IP与端口
        cmd = "i:"+str(request)
        s.sendall(cmd)      #把命令发送给对端
        data=s.recv(1024)     #把接收的数据定义为变量
        print data   
        s.close()
    except Exception,e:
        print Exception,":",e
    return eval(data)
    
def release(args):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
        s.connect((HOST,PORT))       #要连接的IP与端口
        cmd = "r:"+str(args)
        cmd = cmd.replace(" ","");
        s.sendall(cmd)      #把命令发送给对端
        data=s.recv(1024)     #把接收的数据定义为变量
        print data
        s.close()
    except Exception,e:
        print Exception,":",e
    return data

def show(show = True):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
        s.connect((HOST,PORT))       #要连接的IP与端口
        cmd = "s"
        s.sendall(cmd)      #把命令发送给对端
        data=s.recv(1024)     #把接收的数据定义为变量
        sum = 0
        sn_array = []
        data = data.replace(" ","");
        for i,x in enumerate(data):
            if i%2 != 0:
                sn_array.append(int(x))
        num_dict = {}
        for i,x in enumerate(sn_array):
            if x > 0:
                sum += (i+1) * x
                num_dict[i+1] = x
        print 'GPU sum number: '+ str(sum)
        print num_dict
        s.close()
    except Exception,e:
        print Exception,":",e     
    return data
if __name__ == '__main__':
    while 1:
        cmd = raw_input("three options:s(show);r(release);i(request)")
        if cmd.startswith("s"):
            show()
        elif cmd.startswith("r"):
            r = [2,2]
            release(r)
        elif cmd.startswith("i"):            
            request(5)