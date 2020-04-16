

from socket import *
from multiprocessing import Process
import re,time
ADDR = ('0.0.0.0',8888)
user = {}
list_count = []
def do_login(s,name,address):
    if name in user or "管理" in name:
        s.sendto("该用户名已存在".encode(),address)
        return
    else:
        s.sendto(b'OK',address)
        msg = "欢迎%s进入聊天室" % name
        for i in user:
            s.sendto(msg.encode(),user[i])
        user[name]= address

def do_chat(s, name, text):

    pattern = r"xx|aa|bb|oo"
    note = re.findall(pattern,text)
    if note:
        list_count.append(" ".join(note))
        if len(list_count) <3:
            msg = "\n%s注意言辞，被警告%d次"%(name,len(list_count))
            for i in user:
                if i != name:
                    s.sendto(msg.encode(), user[i])
        else:
            do_quit(s,name)
            return
    else:
        msg = "\n%s:%s" % (name, text)
        for i in user:
            if i != name:
                s.sendto(msg.encode(), user[i])

def do_quit(s,name):
    del user[name]
    msg = "\n %s 退出聊天室" % name
    for i in user:
        s.sendto(msg.encode(),user[i])

def manager(s):
    while True:
        msg = input("管理员消息:")
        msg = "C 管理员 " +msg
        s.sendto(msg.encode(),ADDR)

def request(s):

    while True:
        data,addr = s.recvfrom(1024)  # 接收请求
        tmp = data.decode().split(' ',2) # 对请求解析
        if tmp[0] == 'L':
            # 处理进入聊天室 tmp --> ['L', 'name']
            do_login(s,tmp[1],addr)
        elif tmp[0] == 'C':
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            do_quit(s,tmp[1])



def main():

    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    print("等待客户端连接....")
    p = Process(target=request,args=(s,))
    p.start()
    manager(s)
    p.join()

if __name__ == '__main__':
    main()