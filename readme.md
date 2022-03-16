# tcp_emulator_test

## 目录
  * [项目概况](##项目概况)
    + [功能介绍](#功能介绍)
    + [使用教程](#使用教程)
  * [开发文档](#开发文档)
    + [定制开发](#定制开发)
    + [数据库设计](#数据库设计)
  * [附录](#附录)

## 项目概况

该项目提供一个轻量、便捷的**自动化接口测试**框架，用于自动化测试某个目标系统的各种场景TCP报文交互，具有配置简单、零外部依赖、数据可持久化等的优点。

### 功能介绍
在开始深入了解之前，你有必要先知晓该框架的目标功能或使用场景。

开发此项目的初衷，是为了解决本人在开发工作中遇到的一个问题。故事是这样子的：目标系统B是一个中间转发系统，接收来自前置系统A的```Xml```报文，在进行各种处理后组装成```Json```报文转发给后台系统C，且系统B是基于一个高度封装的应用平台构建的，不便使用各种流行的白盒单元测试框架。于是，本人便着手用```Java```开发了一个双端模拟器进行报文收发的工具，最后将这个小工具使用```Python```进行抽象重构。完成了这个项目。它主要提供如下功能。

1. **为开发人员提供一个“先定义接口、后开发功能”场景的开发者手边测试工具。**
2. **克服无法使用或不便于使用类似Junit等单元测试工具的系统进行简单测试。**
3. **自动化功能测试，起到开发进度验收作用。**

接下来，我们来对```tcp_tran_go```进行更深入的了解：

1. 它主要用模拟交互场景来完成测试，查看场景设计(Emulators)了解可以兼容的模拟场景：
    1. 目标系统为client客户端
    2. 目标系统为server服务端
    3. 目标系统为middle中间转发系统


2. 它主要通过SQLite进行数据持久化，查看设计思路（host）了解程序的执行模式：

    1. 主程序通过读取数据库配置来模拟非目标系统（client和server）
    2. 主程序通过读取数据库数据来准备和执行测试案例（case）
    3. 主程序通过更新数据库数据来完成运行历史记录（record、history）



3. 它主要通过自定义配置方式完成模拟场景中模拟系统的功能，查看设计思路（deal）了解你可以为模拟系统配置的自定义功能：
    - 报文创建器：TCP交互前，提供根据模板创建报文的功能。利用seed持续生成不重复报文，例如：用seed来产生报文序列号、请求码等。
    - 报文编码器：TCP交互时，提供发送报文之前进行自定义编码的功能。
    - 报文解码器：TCP交互时，提供接收报文之后进行自定义解码的功能。
    - 报文检查器：TCP交互后，提供对解码后的报文进行自定义检查规则的功能。


### 使用说明
##### ①首先，克隆并进入本项目目录
```shell script
git clone https://gitee.com/zhongshijie/tcp_trans_go.git && cd tcp_trans_go
```

##### ② 新建数据库+创建数据表
```shell script
cd ./_db/ && python insert_table.py && cd ..
```

##### ③ 插入模拟系统配置、案例配置
1. 参考章节**开发文档-编写功能函数**进行相应模拟系统功能开发
2. 参考章节**开发文档-数据库设计**来编辑```data.sql```
3. 运行```insert_data.py```来完成数据插入（也可以直接用你喜欢的数据库管理工具可视化的完成等效操作）。
```shell script
cd ./_db/ && python insert_data.py && cd ..
```

##### ④ 运行目标系统

##### ⑤ 运行主程序

```shell script
python main.py
```
##### ⑥ 完成，等待运行结果

（注：如果你想尝试本人提供的HelloWorld模拟系统和案例，在③环节直接运行```insert_data.py```、④环节直接运行```demo_target.py```即可）

## 开发文档

### 编写功能函数
编写功能函数就是**按照规范编写函数**供模拟系统调用，**赋予模拟系统处理交互报文的能力**。

1. 将功能函数名作为参数被配置在数据表（Emulators）中，使模拟系统在启动时具备这些能力。
2. 这些功能函数都需要在包```./deal/*.py```中的被定义。
3. 建议你使用```系统名称+报文格式```的形式作为函数名，既直观方便，又易于在各个包中进行统一维护。
4. 需要捋清对于server和client而言的预期报文和检查规则。

让我们通过定制开发一个abc系统的xml格式报文的功能函数来了解编写功能函数需要实现的内容和规范吧：

##### ./deal/creator.py

```python
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
```
##### ./deal/encoder.py
```python
def abc_xml(x: str) -> bytes:
    """
    编码abc系统的xml格式报文
    
    将生成的报文以GBK将报文编码为bytes。
    
    :param x: 代编码报文字符串
    :return: 编码后字节流
    """
    return x.encode(encoding='gbk')
```

##### ./deal/decoder.py
```python
def abc_xml(x: bytes) -> str:
    """
    解码abc系统的xml格式报文

    将接收到的报文字节流以GBK解码为报文字符串。

    :param x: 代解码报文字节流
    :return: 解码后的报文字符串
    """
    return x.decode(encoding='gbk')
```

##### ./deal/checker.py
```python
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
```

### 数据库设计
#### EMULATORS
|字段 |描述 |备注 |
|--|--|--|
|EMULATOR_ID |模拟系统ID |默认值：自增长整数 |
|EMULATOR_PACK |模拟系统包名 |可用于标记目标系统 |
|EMULATOR_NAM |模拟系统名 | |
|EMULATOR_SET |模拟系统分类 |可选 client、server |
|EMULATOR_ENABLE |模拟系统启用标识 |1启用-0停用，默认值：1 |
|EMULATOR_SEED |模拟系统种子 |随调用creator自增，可用于生成报文，默认值：0 |
|LISTEN_HOST |监听地址 |如‘127.0.0.1’ |
|LISTEN_PORT |监听端口 |如8888 |
|LISTEN_TYP |监听类型 |S短连接-L长连接，暂未启用（默认不关闭连接） |
|CONN_HOST |连接地址 |如‘127.0.0.1’ |
|CONN_PORT |连接端口 |如9999 |
|CONN_TYP |连接类型 |S短连接-L长连接，暂未启用（默认不关闭连接） |
|ENCODER |编码器名 |对应deal.encoder下的函数名，用于编码报文 |
|DECODER |解码器名 |对应deal.decoder下的函数名，用于解码报文 |
|CHECKER |检查器名 |对应deal.checker下的函数名，用于检查报文 |
|CREATOR |创建器名 |对应deal.creator下的函数名，用于生成报文 |

#### CASES
|字段 |描述 |备注 |
|--|--|--|
|CASE_ID |案例ID |默认值：自增长整数 |
|CASE_PACK |案例包名 |可用于标记分类案例 |
|CASE_NAM |案例名 | |
|CASE_ENABLE |案例启用标识 |1启用-0停用，默认值：1 |
|CLIENT_EMU_ID |client端模拟系统ID | |
|CLIENT_RECV |client端接收报文 | |
|CLIENT_SEND |client端发送报文 | |
|CLIENT_CHECK |client端检查规则 | |
|SERVER_EMU_ID |server端模拟系统ID | |
|SERVER_SEND |server端发送报文 | |
|SERVER_RECV |server端接收报文 | |
|SERVER_CHECK |server端检查规则 | |

#### HISTORY
|字段 |描述 |备注 |
|--|--|--|
|EXEC_ID |执行ID |默认值：自增长整数 |
|EXEC_STATUS |执行状态 |1完成-0待完成，默认值：0 |
|EXEC_TIME_START |执行开始时间 |格式20200101123155 |
|EXEC_TIME_END |执行结束时间 |格式20200101123156 |
|EXEC_RESULT |执行结果 |执行成功率，取值0~1的float |

#### RECORDS
|字段 |描述 |备注 |
|--|--|--|
|RECORD_ID |记录ID |默认值：自增长整数 |
|EXEC_ID |执行ID | |
|CASE_ID |案例ID | |
|EMULATORS_ID |模拟系统ID | |
|RECORD_SEND_REL |发送内容 | |
|RECORD_RECV_REL |接收内容 | |
|RECORD_RESULT |检查结果 |Accept成功-否则为失败 |


## 附录
-  ```./_db/create.sql```，建表脚本：用于创建项目项目所需的所有表。
-  ```./_db/data.sql```，数据脚本：用于插入demo目标系统的测试案例。
-  ```./demo_target.py```，运行脚本：用于运行demo目标系统。


# tcp_proxy
纯Python完成的TCP转发代理，Nginx进行TCP端口转发不便于篡改报文内容，本项目提供可篡改报文内容的TCP转发代理。

## 运行说明
0. 安装Python
1. 编辑`info.py`中的配置内容
2. 运行`sh run.sh`，运行日志文件为`tcp_proxy.log`


## 定制说明
> 通过修改`_conf.py`完成定制，以下为样例代码

1. 直接转发
  ```python
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
      return msg
   ```
2. 篡改TCP报文内文本XML节点的文本为指定值：
  ```python
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
  ```
