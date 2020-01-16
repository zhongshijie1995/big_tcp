# 数据库地址（绝对目录）
db_file = './_db/db.sqlite3'
db_path = '由主函数运行时确定该目录并赋值'

# 线程在线列表
thread_list = []

# 模拟系统配置
max_listen = 100

# 标志
accept_flag = 'Accept'
end_flag = 'finish'

# 表值
client = 'client'
server = 'server'
# 表字段-EMULATORS
emulator_id = 'EMULATOR_ID'
emulator_set = 'EMULATOR_SET'
emulator_nam = 'EMULATOR_NAM'
emulator_seed = 'EMULATOR_SEED'
listen_host = 'LISTEN_HOST'
listen_port = 'LISTEN_PORT'
conn_host = 'CONN_HOST'
conn_port = 'CONN_PORT'
encoder = 'ENCODER'
decoder = 'DECODER'
creator = 'CREATOR'
checker = 'CHECKER'
# 表字段-CASES
case_id = 'CASE_ID'
case_pack = 'CASE_PACK'
case_nam = 'CASE_NAM'
client_emu_id = 'CLIENT_EMU_ID'
client_recv = 'CLIENT_RECV'
client_send = 'CLIENT_SEND'
client_check = 'CLIENT_CHECK'
server_emu_id = 'SERVER_EMU_ID'
server_recv = 'SERVER_RECV'
server_send = 'SERVER_SEND'
server_check = 'SERVER_CHECK'
# 表字段HISTORY
exec_id = 'EXEC_ID'
# 表字段RECORDS
record_result = 'RECORD_RESULT'

# 查询语句
query_emulators = 'SELECT * FROM EMULATORS WHERE EMULATOR_ENABLE = 1'
query_cases = 'SELECT * FROM CASES WHERE CASE_ENABLE = 1'
query_emulators_nam = 'SELECT EMULATOR_NAM FROM EMULATORS WHERE EMULATOR_ID = ?'
query_history_max_id = 'SELECT MAX(EXEC_ID) FROM HISTORY'
query_records = 'SELECT * FROM RECORDS WHERE EXEC_ID=?'
# 插入语句
create_history = 'INSERT INTO HISTORY (EXEC_TIME_START) VALUES (?)'
create_record = 'INSERT INTO RECORDS (EXEC_ID, CASE_ID, EMULATORS_ID, RECORD_SEND_REL, RECORD_RECV_REL, ' \
                'RECORD_RESULT) VALUES (?, ?, ?, ?, ?, ?) '
# 更新语句
update_history = 'UPDATE HISTORY SET EXEC_STATUS=?, EXEC_TIME_END=?, EXEC_RESULT=? WHERE EXEC_ID=?'
update_seed = 'UPDATE EMULATORS SET EMULATOR_SEED=? WHERE EMULATOR_ID=?'
