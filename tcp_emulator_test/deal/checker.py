from const import Val


def abc_xml(x: str, y: str, chk_set: str) -> str:
    """
    根据检查规则，检查接收到的abc系统的xml格式报文

    若匹配规则为equals，则当预期和接收报文完全相等时返回accept常量；否则返回它们的拼接可用对比差异。

    :param x: 预期内容字符串
    :param y: 实际内容字符串
    :param chk_set: 匹配规则字符串
    :return:
    """
    if chk_set == 'equals' and x == y:
        return Val.accept_flag
    return '{}/{}'.format(x, y)


def odfs_json(x: str, y: str, chk_set: str) -> str:
    if x == y:
        return Val.accept_flag
    return '{}/{}'.format(x, y)
