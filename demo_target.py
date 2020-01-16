import socket
import time


if __name__ == '__main__':
    listen = socket.socket()
    listen.bind(('127.0.0.1', 18999))
    listen.listen(10)
    while True:
        client, addr = listen.accept()
        recv = client.recv(1024).decode('gbk')
        time.sleep(2)
        conn = socket.socket()
        conn.connect(('127.0.0.1', 20000))
        conn.send(recv.replace('他', '我').encode('gbk'))
        x = conn.recv(2048)
        client.send(x)
