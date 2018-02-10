
# eagle-oj-judger

## Document

You can see document in http://docs.eagleoj.com/#/en/judger .

## You don't need to read following things

### 环境安装

我们使用Ubuntu16.04已经通过测试

```bash
apt update
apt install -y python
apt install -y python3
apt install -y openjdk-8-jre
apt install -y openjdk-8-jdk
apt install -y cmake
apt install -y gcc
apt install -y g++
pip install -y flask
pip install -y gunicorn
pip install -y gevent
```
1.Build

`sudo apt-get install libseccomp-dev`

`mkdir build && cd build && cmake .. && make && sudo make install`
2.python binding

`sudo python setup.py install  #位于eagle-oj-judger/bindings/Python/目录`

3.add server packge and model packge to python environemnt

`sudo python3 initEnv.py #位于eagle-oj-judger/Judger/server/目录下`

4.Edit gunicorn.conf

```python
import os  
bind = '0.0.0.0:5000'  #注意将这里的IP修改为自己本机的IP或者直接127.O.0.1:5000，端口号自定义  
workers = 4     #进程数  
backlog  = 2048      #监听队列  
worker_class = "gevent"  #使用gevent模式，还可以使用sync 模式，默认的是sync模式  
debug = True  
chdir = '/usr/Judger/Judger' #Client.py所在位置  
proc_name = 'gunicorn.proc'
```
5.install virtualenv
```bash
pip3 install virtualenv #如果已经安装virtualenv则跳过此步
cd /usr && mkdir myenv  && cd mkdir   
virtualenv -p /usr/bin/python3.5 py3env  #创建Python3.5虚拟环境   
virtualenv --system-site-packages py3env #将本地pyton3.5所有的包添加到虚拟环境当中  
cd py3env && source bin/activate #进入到虚拟环境的文件夹并且启动虚拟环境    
deactivate #如果需要退出虚拟环境执行该命令 
```
6.launch the judger
`gunicorn -k gevent -c gunicorn.conf Client:app #进入到Judger目录下在终端输入一下命令,并且需要在虚拟环境激活的情况下令`

### 判卷机说明

本判卷系统核心部分使用的是青岛大学的OJ判卷系统，在安装过程中如果出现疑问地方。[可以点击这里](http://docs.onlinejudge.me/#/judger/api)。

## 系统说明
1. **语言支持**:
    - python3.5
    - python2.7
    - Java8
    - C++
    - C

2. **sys_config**：
	-  outfile为提交带代码所产生的临时文件存放路径
	-  removefile：每次判断后是否删除文件,默认为True,即每次都删除
	-  server:server包的路径
	-  model:model包的路径
	-  uid:执行代码的uid
	-  gid:用于执行代码的gid
3. **表单传输字段说明**:

```
 {
    "lang": "PYTHON35",  
    "source_code": "print('hello')",  
    "time_limit": "3",  
    "memory_limit": "128",  
    "test_cases": [  
      {  
        "stdin":"123  
        "stdout": "hello"  
      },  
      {
        "stdin": "123",  
        "stdout": "hello"  
      },  
      {   
        "stdin": "5",  
        "stdout": "hello"  
      }  
    ]  
  }

```

  - lang:编程语言种类
  - source_code:需要提交的代码
  - time_limit:运行时间限制
  - memory_limit:内存限制
  - test_cases:所有测试例子
      1. stdin:标准输入值
      2. stdout:期望输出值

4. **返回结果值**：
```
{  
    "test_cases": [  
        {  
            "result": "AC",  
            "error_message": null  
        },  
        {  
            "result": "AC",  
            "error_message": null  
        },
        {  
            "result": "AC",  
            "error_message": null  
        }  
    ],  
    "result": "AC",  
    "available_memeory": 5.26,  
    "memory": 3,  
    "time": 0,  
    "memory_percent": "31.6%"  
}

```

 -  test_cases:
  1. result：测试点结果
  2. error_message: 测试点异常信息
 -  result:判卷结果
 -  available_memeory:系统可用内存,单位GB
 -  memory: 程序所需内存
 -  time:程序运行时间（0的情况是因为时间太短）
 -  memory_percent:百分比内存情况

5. **运行结果说明**：
    - AC：Accept 即通过
    - RTE: Runtime Eroor 运行时错误
    - SE: System Error 系统错误
    - TLE:Time Limit Error 运行超时错误
    - CE: Compile Error 编译错误
