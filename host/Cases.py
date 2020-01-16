from utils import Log
from utils import Db
from const import Val
import threading


def make_task(exec_id: int, row: dict, target: str) -> dict:
    result = {}
    target = target.upper()
    for col in row:
        if col.startswith(target):
            result[col] = row[col]
    result[Val.case_id] = row[Val.case_id]
    result[Val.exec_id] = exec_id
    return result


def goes_cases(exec_id: int, eqd: dict) -> None:
    db = Db.Db(Val.db_path)
    rows = db.get_rows(Val.query_cases)
    for row in rows:
        case_id = row.get(Val.case_id)
        case_pack = row.get(Val.case_pack)
        case_nam = row.get(Val.case_nam)
        Log.debug('读取案例 {}-{}-{}'.format(case_id, case_pack, case_nam))
        cn = db.get_one_val(Val.query_emulators_nam, (row[Val.client_emu_id],))
        sn = db.get_one_val(Val.query_emulators_nam, (row[Val.server_emu_id],))
        if cn is not None:
            task = make_task(exec_id, row, Val.client)
            Log.debug('添加任务 {} {} - {} {}'.format(case_pack, case_nam, cn, task))
            eqd[cn].put(task)
        if sn is not None:
            task = make_task(exec_id, row, Val.server)
            Log.debug('添加任务 {} {} - {} {}'.format(case_pack, case_nam, sn, task))
            eqd[sn].put(task)
    db.close()


def finish_cases(emulators_queue_dict):
    for em in emulators_queue_dict:
        emulators_queue_dict[em].put(Val.end_flag)


class HostCases(threading.Thread):
    def __init__(self, exec_id, emulators_queue_dict):
        self.exec_id = exec_id
        self.emulators_queue_dict = emulators_queue_dict
        threading.Thread.__init__(self)

    def run(self) -> None:
        goes_cases(self.exec_id, self.emulators_queue_dict)
        finish_cases(self.emulators_queue_dict)


def run_cases(exec_id, emulators_queue_dict):
    e = HostCases(exec_id, emulators_queue_dict)
    e.start()
    Val.thread_list.append(e)


if __name__ == '__main__':
    pass
