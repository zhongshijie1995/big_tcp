from utils import Db
from utils import Log
from const import Val
import time


def init_history() -> int:
    # 建立数据库连接
    db = Db.Db(Val.db_path)
    # 生成内容
    exec_time_start = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 执行更新
    db.exec(Val.create_history, (exec_time_start, ))
    db.commit()
    # 获取执行序列号
    exec_id = int(db.get_one_val(Val.query_history_max_id))
    # 关闭数据库连接
    db.close()
    return exec_id


def update_history(exec_id) -> None:
    def compute_result(rows: list) -> float:
        # 整理案例分数字典
        compute_dict = {}
        for row in rows:
            case_id = row[Val.case_id]
            chk_score = 0 if row[Val.record_result] == Val.accept_flag else -1
            if case_id in compute_dict:
                compute_dict[case_id] += chk_score
            else:
                compute_dict[case_id] = chk_score
        # 计算执行结果
        denominator = len(compute_dict)
        if denominator == 0:
            denominator = float('inf')
        numerator = 0
        for case_id in compute_dict:
            if compute_dict[case_id] == 0:
                numerator += 1
        result = numerator / denominator
        Log.info('执行序列号 {} 共执行 {} 条，计算结果为 {}'.format(exec_id, denominator, format(result, '.2%')))
        return result
    # 等待主持线程结束
    for t in Val.thread_list:
        t.join()
    # 建立数据库连接
    db = Db.Db(Val.db_path)
    # 生成内容
    exec_status = 1
    exec_time_end = time.strftime("%Y%m%d%H%M%S", time.localtime())
    exec_result = compute_result(db.get_rows(Val.query_records, (exec_id, )))
    # 执行更新
    db.exec(Val.update_history, (exec_status, exec_time_end, exec_result, exec_id))
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    print(init_history())
