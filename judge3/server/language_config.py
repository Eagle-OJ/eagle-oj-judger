
config={
    #设置代码，测试用例等文件的位置
    'outfile':'/usr/JudgeResult',
    'JAVA8':{
        'exe_path':'/usr/bin/java',
        'max_memory':-1,
        'source_name':'Main.java',
        'complication':True,
        'compile_command':'javac {exe_path}/Main.java',
        'run':{
            'args':'-cp {exe_path} -Xss1M -XX:MetaspaceSize=64m -XX:MaxMetaspaceSize=128m -Xms128M -Xmx{max_memory}M Main',
            'seccomp_rule':None,
        }
    },
    'PYTHON36':{
        'exe_path':'/usr/bin/python3.5',
        'max_memory': 128 * 1024 * 1024,
        'source_name':'Main.py',
        'complication': False,
        'compile_command': None,
        'run':{
            'args':'{exe_path}/Main.py',
            'seccomp_rule': 'general',
        }
    },
    'C':{
        'exe_path':'{exe_path}/Main',
        'max_memory':128 * 1024 * 1024,
        'source_name':'Main.c',
        'complication':True,
        'compile_command':'gcc {exe_path}/Main.c -o {exe_path}/Main',
        'run':{
            'args':'',
            'seccomp_rule':'c_cpp',
        }
    },
    'CPP':{
        'exe_path': '{exe_path}/Main',
        'max_memory': 128 * 1024 * 1024,
        'source_name': 'Main.cpp',
        'complication': True,
        'compile_command': 'g++ {exe_path}/Main.cpp -o {exe_path}/Main',
        'run': {
            'args': '',
            'seccomp_rule': 'c_cpp',
        }
    },
    'PYTHON27':{
        'exe_path':'/usr/bin/python2.7',
        'max_memory': 128 * 1024 * 1024,
        'source_name':'Main.py',
        'complication': False,
        'compile_command':None,
        'run':{
            'args':'{exe_path}/Main.py',
            'seccomp_rule': 'general',
        }
    }
}
