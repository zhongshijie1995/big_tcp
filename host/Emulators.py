from utils import Log
from utils import Db
from const import Val
from deal import creator, decoder, encoder, checker
import socket
import threading
import queue


def call_deal(o_nam: str, f_nam: str, args: tuple) -> bytes:
    content = eval('{}.{}'.format(o_nam, f_nam))(*args)
    return content


class ClientEmulator(threading.Thread):
    def __init__(self, q, row) -> None:
        self.q = q
        self.row = row
        self.typ = row[Val.emulator_set]
        self.nam = row[Val.emulator_nam]
        self.host = row[Val.conn_host]
        self.port = row[Val.conn_port]
        self.id = row[Val.emulator_id]
        self.encoder = row[Val.encoder]
        self.decoder = row[Val.decoder]
        self.creator = row[Val.creator]
        self.checker = row[Val.checker]
        self.emulator_seed = row[Val.emulator_seed]
        threading.Thread.__init__(self)

    def run(self) -> None:
        Log.info('开始配置模拟系统 {} {} {} {}'.format(self.typ, self.nam, self.host, self.port))
        while True:
            task = self.q.get(block=True)
            if task == Val.end_flag:
                break
            self.run_task(task)

    def run_task(self, task):
        # 建立连接
        s = socket.socket()
        Log.debug('{} 发起连接 {} {}'.format(self.nam, self.host, self.port))
        s.connect((self.host, self.port))
        # 准备内容
        content = call_deal('creator', self.creator, (task[Val.client_send], self.emulator_seed))
        self.emulator_seed += 1
        Log.info('{} 准备内容 {}'.format(self.nam, content))
        # 编码并发送
        content_send = call_deal('encoder', self.encoder, (content, ))
        s.send(content_send)
        Log.info('{} 发送内容 {}'.format(self.nam, content))
        # 接收并解码
        recv = s.recv(2048)
        recv = call_deal('decoder', self.decoder, (recv, ))
        Log.info('{} 收到返回 {}'.format(self.nam, recv))
        # 检查接收内容
        chk_r = call_deal('checker', self.checker, (recv, task[Val.client_recv], task[Val.client_check]))
        Log.info('{} 进行检查 {}'.format(self.nam, chk_r))
        # 关闭连接
        s.close()
        Log.debug('{} 断开连接 {} {}'.format(self.nam, self.host, self.port))
        # 进行记录
        db = Db.Db(Val.db_path)
        db.exec(Val.create_record, (task[Val.exec_id], task[Val.case_id], self.id, content, recv, chk_r))
        db.exec(Val.update_seed, (self.emulator_seed, self.id))
        db.commit()
        Log.info('{} 完成案例 {}'.format(self.nam, task[Val.case_id]))


class ServerEmulator(threading.Thread):
    def __init__(self, q, row) -> None:
        self.q = q
        self.typ = row[Val.emulator_set]
        self.nam = row[Val.emulator_nam]
        self.host = row[Val.listen_host]
        self.port = row[Val.listen_port]
        self.id = row[Val.emulator_id]
        self.encoder = row[Val.encoder]
        self.decoder = row[Val.decoder]
        self.creator = row[Val.creator]
        self.checker = row[Val.checker]
        self.emulator_seed = row[Val.emulator_seed]
        threading.Thread.__init__(self)

    def run(self) -> None:
        Log.info('开始配置模拟系统 {} {} {} {}'.format(self.typ, self.nam, self.host, self.port))
        self.run_task()

    def run_task(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(Val.max_listen)
        while True:
            task = self.q.get(block=True)
            if task == Val.end_flag:
                s.close()
                break
            # 获取连接
            client, addr = s.accept()
            Log.debug('{} 获取到连接 {} {}'.format(self.nam, addr[0], addr[1]))
            # 接收并解码
            recv = client.recv(2048)
            recv = call_deal('decoder', self.decoder, (recv, ))
            Log.info('{} 收到内容 {}'.format(self.nam, recv))
            # 检查接收内容
            chk_r = call_deal('checker', self.checker, (recv, task[Val.server_recv], task[Val.server_check]))
            Log.info('{} 进行检查 {}'.format(self.nam, chk_r))
            # 准备内容
            reply = call_deal('creator', self.creator, (task[Val.server_send], self.emulator_seed, recv))
            self.emulator_seed += 1
            Log.info('{} 准备内容 {}'.format(self.nam, reply))
            # 编码并发送
            reply_send = call_deal('encoder', self.encoder, (reply, ))
            client.send(reply_send)
            Log.info('{} 返回内容 {}'.format(self.nam, reply))
            # 进行记录
            db = Db.Db(Val.db_path)
            db.exec(Val.create_record, (task[Val.exec_id], task[Val.case_id], self.id, reply, recv, chk_r))
            db.exec(Val.update_seed, (self.emulator_seed, self.id))
            db.commit()
            Log.info('{} 完成案例 {}'.format(self.nam, task[Val.case_id]))


def create_emulator(row) -> queue.Queue:
    typ = row[Val.emulator_set]
    q = queue.Queue()
    if Val.client in typ:
        e = ClientEmulator(q, row)
        e.start()
        Val.thread_list.append(e)
    elif Val.server in typ:
        e = ServerEmulator(q, row)
        e.start()
        Val.thread_list.append(e)
    else:
        Log.critical('出现分类不明确的模拟系统配置 {}'.format(typ))
    return q


def run_emulator() -> dict:
    db = Db.Db(Val.db_path)
    rows = db.get_rows(Val.query_emulators)
    emulator_queue_dict = {}
    for row in rows:
        emulator_queue_dict[row[Val.emulator_nam]] = create_emulator(row)
    db.close()
    return emulator_queue_dict


if __name__ == '__main__':
    r = call_deal('abc_xml', ('xxxa', 1))
    print(r)
