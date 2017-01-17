# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket   #socket模块

class resource:
    #定义基本属性, 第i个数组的值代表有i+1个GPU的机器的数目
    sn_array = []
    def __init__(self, sn_array_p):
        self.sn_array= [sn for sn in sn_array_p]
    def allocate(self, sum_num):
        result = []
        source_p = []
        #把资源展开放在数组中去，并按照从大到小的顺序排列
        for i,x in enumerate(self.sn_array):
            if x > 0:
                for n in range(0, x):
                    source_p.append(i+1)
        #然后从大到小，满足要求就拿，并且和之前的比较
        source_p = source_p[::-1]
        print self.sn_array
        print source_p
        for tmp in source_p:
            if sum(result) < sum_num:
                result.append(tmp)
            elif sum(result) == sum_num:
                break
            else:
                result.append(tmp)
                spare_num = sum(result) - sum_num
                #这个时候策略就是逐渐降低总和
                for t in result:
                    if t <= spare_num:
                        result.remove(t)
                        break
        for t in result:
            self.sn_array[t-1] -= 1
        print self.sn_array
        return result
    def release(self, rsn_array):
        for item in rsn_array:
            self.sn_array[item-1] += 1
        print self.sn_array
        
    def show(self):
        #第一行是总的GPU数目，
        #第二行是一个字典，{x: y}  x是节点上GPU的数目，y是当前这种节点的个数
        sum = 0
        num_dict = {}
        for i,x in enumerate(self.sn_array):
            if x > 0:
                sum += (i+1) * x
                num_dict[i+1] = x
        print 'GPU sum number: '+ str(sum)
        print num_dict
        return self.sn_array
        
def initialResource(*array):
    initial = [0,0,0,0,0]    
    for m in array[0]:
        initial[m-1] += 1
    return initial
   
res = [1,1,1,2,2,2,2,3,3,4,4,4]     
#initial = [3,4,5,1,0]
initial = initialResource(res)
print initial
#release = [3,4,5,7,3]
res_pool = resource(initial)
res_pool.show()
#print test.sn_array
HOST='127.0.0.1'
PORT=50007
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
s.bind((HOST,PORT))   #套接字绑定的IP与端口
s.listen(1)         #开始TCP监听
while 1:
    try:
        conn,addr=s.accept()   #接受TCP连接，并返回新的套接字与IP地址
        print'Connected by',addr    #输出客户端的IP地址
        data=str(conn.recv(1024))    #把接收的数据实例化
        print data
        if data.startswith("i"):
            number = int(data[2:])
            print "number,", number
            result = res_pool.allocate(number)
            conn.sendall(str(result))
        elif data.startswith("r"):
            rel_array = []
            num_array = data[2:]
            for i,x in enumerate(num_array):
                if i%2 != 0:
                    rel_array.append(int(x))
            res_pool.release(rel_array)
            conn.sendall(str(res_pool.sn_array))
        elif data.startswith("s"):
#                res_pool.show()
            print str(res_pool.sn_array)
            conn.sendall(str(res_pool.sn_array))
        conn.close()     #关闭连接
    except Exception,e:
        print Exception,":",e
        