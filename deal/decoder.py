def abc_xml(x: bytes) -> str:
    """
    解码abc系统的xml格式报文

    将接收到的报文字节流以GBK解码为报文字符串。

    :param x: 代解码报文字节流
    :return: 解码后的报文字符串
    """
    return x.decode(encoding='gbk')


def odfs_json(x: bytes) -> str:
    return x.decode(encoding='gbk')
