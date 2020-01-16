import re


def abc_xml(x: str, seed: int, y: str = '') -> str:
    """
    创建abc系统的xml格式报文

    利用seed种子值生成了一个6位的循环数字，用于替换xml报文中的ReqSeq内的请求序号号，每次创建不同的报文。

    :param x: 模板报文字符串
    :param seed: 模拟器种子值
    :param y: 接收报文字符串（仅当模拟器类型为server时传入）
    :return: 生成报文字符串
    """
    seq_no = str(seed % 999999).zfill(6)
    p = re.compile(r"(?<=<ReqSeq>).+?(?=</ReqSeq>)")
    return re.sub(p, seq_no, x)


def odfs_json(tmp: str, seed: int, y: str = '') -> str:
    return tmp.upper()
