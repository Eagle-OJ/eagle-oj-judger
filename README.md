# eagle-oj-judger
基于Restful的开源判卷核心

1.Build
>sudo apt-get install libseccomp-dev
mkdir build && cd build && cmake .. && make && sudo make install

2.python binding
>sudo python setup.py install

3.add server packge and model packge to python environemnt
> sudo python3 initEnv.py 
可在/judge3/server/config中的sys_config修改名称

4.Get IP
> sudo ip address
> 获取IP地址并且可以添加到judge3/gunicorn中

5.Edit gunicorn.conf

>import os
bind = '10.151.26.112:5000'   #绑定的ip及端口号，需要设置端口对开开放或者可以直接诶配置为127.0.0.1:5000
workers = 4     #进程数
backlog = 2048      #监听队列
worker_class = "gevent"     #使用gevent模式，还可以使用sync 模式，默认的是sync模式
debug = True
chdir = '/usr/Judger/judge3' #Client.py所在位置
proc_name = 'gunicorn.proc'

6.launch the judger
> gunicorn -k gevent -c gunicorn.conf Client:app#进入到judge3目录下在终端输入一下命令


### 系统说明
1. 目前支持python36,java8,python27,c,c++五种编程语言.
2. sys_config说明：
	1.  outfile为提交带代码所产生的临时文件存放路径
	2.  removefile：每次判断后是否删除文件,默认为True,即每次都删除
	3.  server:server包的路径
	4.  model:model包的路径
3.  表单传输字段说明:
> 
 {
    "lang": "CPP",
    "source_code": "#include<iostream>\nusing namespace std;int main(){cout<<\"hello\"<<endl;return 0;}",
    "time_limit": "3",
    "memory_limit": "128",
    "test_cases": [
      {
        "stdin":"123",
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
  
  1. lang:编程语言种类
  2. source_code:需要提交的代码
  3. time_limit:运行时间限制
  4. memory_limit:内存限制
  5. test_cases:所有测试例子
  6. stdin:标准输入值
  7. stdout:期望输出值

4.返回结果值说明：
> 
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

1. test_cases:
	1. result：测试点结果
	2. error_message: 测试点异常信息
2. result:判卷结果
3. available_memeory:系统可用内存,单位GB
4. memory: 程序所需内存
5. time:程序运行时间（0的情况是因为时间太短）
6. memory_percent:百分比内存情况
