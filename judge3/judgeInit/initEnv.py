from server.config import sys_config

#请在sudo命令和python3.5的环境下执行

#将server包以及model包添加到python环境当中
with open('/usr/local/lib/python3.5/dist-packages/JudgePath.pth','a') as file:
    file.write(sys_config['model'])
    file.write(sys_config['server'])
