import re


# 代理最大连接数
MAX_PROXY = 200
# 代理服务器
PROXY_HOST = '0.0.0.0'
PROXY_PORT = 20001
# 目标服务器
DEST_HOST = '192.168.0.101'
DEST_PORT = 20001


def deal_msg(msg: bytes) -> bytes:
    """
    代理服务器处理TCP文本定制函数

    :param msg:
    :return:
    """
    # 报文头长度和编码
    head_len = 4
    encoding = 'utf-8'
    # 分离报文头和报文体，解码报文体
    msg_head = msg[:head_len]
    msg_body = msg[head_len:].decode(encoding)
    # 替换指定xml标签内的文本
    acc_date = '20210531'
    tag_list = [
        r'(?<=<v_date>).+?(?=</v_date>)',
        r'(?<=<value_date>).+?(?=</value_date>)',
    ]
    for tag in tag_list:
        msg_body = re.sub(tag, acc_date, msg_body)
    # 编码报文体
    msg_body = msg_body.encode(encoding)
    # 拼接报文头和报文体
    return msg_head + msg_body
