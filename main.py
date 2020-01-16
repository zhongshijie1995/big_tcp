import os
from const import Val
from host import Emulators
from host import Cases
from host import Records


if __name__ == '__main__':
    # 赋值数据库路径
    Val.db_path = os.path.abspath(Val.db_file)

    # 准备运行历史参数
    exec_id = Records.init_history()

    # 启动模拟系统
    emulators_queue_dict = Emulators.run_emulator()

    # 启动运行器
    Cases.run_cases(exec_id, emulators_queue_dict)

    # 更新运行历史
    Records.update_history(exec_id)
