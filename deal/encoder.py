def abc_xml(x: str) -> bytes:
    """
    编码abc系统的xml格式报文

    将生成的报文以GBK将报文编码为bytes。

    :param x: 代编码报文字符串
    :return: 编码后字节流
    """
    return x.encode(encoding='gbk')


def odfs_json(x: str) -> bytes:
    return x.encode(encoding='gbk')
