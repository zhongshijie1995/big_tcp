import socket
import time
import re


# 代理最大连接数
MAX_PROXY = 200
# 代理服务器
PROXY_HOST = '0.0.0.0'
PROXY_PORT = 20001
# 目标服务器
DEST_HOST = '10.225.142.234'
DEST_PORT = 20001


# 报文编码
SKIP_BYTES_COUNT = 4
DEAL_ENCODE = 'utf-8'


def deal_msg(msg: bytes) -> bytes:
    """
    代理服务器处理TCP文本定制函数

    :param msg:
    :return:
    """
    msg_len = msg[:SKIP_BYTES_COUNT]
    msg = msg[SKIP_BYTES_COUNT:].decode(DEAL_ENCODE)
    acc_date = '20210531'
    p = r"(?<=<v_date>).+?(?=</v_date>)"
    msg = re.sub(p, acc_date, msg)
    p = r"(?<=<value_date>).+?(?=</value_date>)"
    msg = re.sub(p, acc_date, msg)
    return msg_len + msg.encode(DEAL_ENCODE)


class LogClass(object):
    def __init__(self):
        pass

    def inner_log(msg: str) -> None:
        """
        内建日志函数

        :param msg:
        :return:
        """
        with open('tcp_proxy.log', encoding='utf-8', mode='a') as f:
            text = time.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + msg
            text += '\n'
            f.write(text)


class ProxyClient(object):
    """
    代理客户端，扮演与远程目标交互的角色
    """
    def __init__(self, host: str, port: int):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port), )
            LogClass.inner_log('代理客户端已连接到 %s:%s' % (host, port))
        except Exception as e:
            LogClass.inner_log('代理客户端连接远程失败【%s】' % e)

    def send_and_recv(self, msg_out: bytes) -> bytes:
        try:
            LogClass.inner_log('代理客户端发送报文【%s】' % msg_out)
            self.client.sendall(msg_out)
            msg_in = self.client.recv(1024000)
            LogClass.inner_log('代理客户端收到报文【%s】' % msg_in)
        finally:
            LogClass.inner_log('关闭代理客户端')
            self.client.close()
        return msg_in


class ProxyServer(object):
    """
    代理服务器，扮演与连接请求方交互的角色
    """
    def __init__(self, host: str, port: int) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port), )
        self.server.listen(MAX_PROXY)
        LogClass.inner_log('代理服务器已启动 %s:%s' % (host, port))

    def proxy(self, host: str, port: int) -> None:
        try:
            # 主循环
            while True:
                # 代理服务器等待转发任务
                sock, address = self.server.accept()
                msg_out = sock.recv(1024000)
                # 代理服务处理转发任务
                LogClass.inner_log('代理服务器接收到转发任务 %s' % str(address))
                LogClass.inner_log('转发任务原始报文【%s】' % msg_out)
                msg_out = deal_msg(msg_out)
                LogClass.inner_log('转发任务最终报文【%s】' % msg_out)
                LogClass.inner_log('代理服务器将报文转发到 %s:%s' % (host, port))
                try:
                    client = ProxyClient(host, port)
                    msg_in = client.send_and_recv(msg_out)
                except Exception as e:
                    msg_in = msg_out
                    LogClass.inner_log('代理客户端转发到目标失败【%s】，舍弃本次转发，直接应答原包' % str(e))
                # 代理服务器应答转发任务
                LogClass.inner_log('代理服务器将代理客户端收到的报文应答给 %s' % str(address))
                sock.sendall(msg_in)
                # 断开本次连接
                sock.close()
        finally:
            LogClass.inner_log('关闭代理服务器')
            self.server.close()


if __name__ == '__main__':
    s = ProxyServer(PROXY_HOST, PROXY_PORT)
    s.proxy(DEST_HOST, DEST_PORT)
