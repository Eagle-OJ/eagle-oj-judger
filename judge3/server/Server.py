import uuid
import subprocess
import os
import _judger
import shutil
from server.Factory import LanguageFactory
from server.CodeResultEnum import CodeResult
from server.language_config import config

class JudgeServer:

    def __init__(self,data):
        self.data =data

    def make_dir(self,outfile):
        count = 0
        fileName = outfile+str(uuid.uuid1())
        # fileName = outFile+'1'
        stdout = fileName+'/stdout/'
        stdin = fileName+'/stdin/'
        # 以uuid创建一个文件
        if not os.path.exists(fileName):
            os.mkdir(fileName)

            os.mkdir(fileName+'/stderr/')
            os.mkdir(fileName+'/factout/')
            os.mkdir(stdin)
            os.mkdir(stdout)
        for item in self.data['test_cases']:
            self.writeFile(fileName=stdin+str(count),fileContent=item['stdin'],suffix='.in')
            self.writeFile(fileName=stdout+str(count),fileContent=item['stdout'],suffix='.out')
            count = count+1
        #返回该文件夹的父文件
        return fileName

    def writeFile(self,fileName, fileContent, suffix=''):
        with open(str(fileName) + suffix, 'w',encoding='utf-8') as file:
            file.write(fileContent)

    def judge(self):
        # outfile = 'E:/JudgeResult/'
        outfile = config['outfile']
        #存放每个测试用例的结果
        test_cases_result = []
        #默认判断结果返回值为'AC
        total_result = 'AC'
        #用于记录判卷总时间
        time = 0
        #用于记录判断总内存
        memory = 0
        test_cases_num = len(self.data['test_cases'])
        #获得测试用例个数
        filename = self.make_dir(outfile)
        #获取创建的文件夹名
        lang = self.data['lang']
        #根据json去工厂当中获取对应对象
        language_factory = LanguageFactory(language=lang,outfile=filename)
        #参数为可选参数，因为在java当中需要手动设置内存
        language = language_factory.get_obj(max_memory=self.data['memory_limit'])
        #write sourcecode,the content is gotten from data['source_code']
        self.writeFile(fileName=filename + '/' + language.getSourceName(), fileContent=self.data['source_code'])


        for i in range(0,test_cases_num):
            run_result = self.runCode(language, 
                                        stdin=filename + '/stdin/' + str(i) + '.in',
                                        factout=filename + '/factout/' + str(i) + '.out',
                                        stderr=filename + '/stderr/' + str(i) + '.out',
                                        stdout=filename + '/stdout/' + str(i) + '.out',
                                        time_limit=int(self.data['time_limit']) * 1000
                                      )
            if (len(run_result) == 2):
                test_cases_result.append(run_result)
                continue
            # 如果返回值的长度为2，说明判卷出现了异常情况
            time = run_result['time'] + time
            memory = run_result['memory'] + memory
            run_result.pop('time')
            run_result.pop('memory')
            test_cases_result.append(run_result)
        for item in test_cases_result:
            if (item['result'] != 'AC'):
                total_result = item['result']
                break
        result = {
            'time': round(time / test_cases_num, 2),
            'memory': int(memory / test_cases_num),
            'result': total_result,
            'test_case': test_cases_result
        }
        #remove the directory
        shutil.rmtree(filename)
        return result

    def runCode(self,language,**kwargs):
        if (language.getComplication() == True):
            compileErrorResult = self.checkRunnable(language.getCompileCommand())
            if compileErrorResult != '':
                return {'result':'CE',
                        'error_message':compileErrorResult}
        # else:
        # ret = {'cpu_time': 0,
        #        'signal': 0,
        #        'memory': 4554752,
        #        'exit_code': 0,
        #        'result': 2,
        #        'error': 0,
        #        'real_time': 2000}
        ret = _judger.run(max_cpu_time=1000,
                          max_real_time=kwargs['time_limit'],
                          max_memory=language.getMax_memory(),
                          max_process_number=200,
                          max_output_size=10000,
                          max_stack=32 * 1024 * 1024,
                          # five args above can be _judger.UNLIMITED
                          exe_path=language.getExe_path(),
                          input_path=kwargs['stdin'],
                          output_path=kwargs['factout'],
                          error_path=kwargs['stderr'],
                          args=language.getRun_args(),
                          # args=[],
                          # can be empty list
                          env=[],
                          log_path="judger.log",
                          # can be None
                          seccomp_rule_name=language.getRun_rule(),
                          uid=1001,
                          gid=1001)
        if ret['result'] == CodeResult.SYSTEM_ERROR:
            return {'result': 'SE',
                    'error_message': 'System Error'}

        if ret['result'] == CodeResult.RUNTIME_ERROR:
            with open(kwargs['stderr'], 'r', encoding='utf-8') as file:
                error_message = ''
                for line in file:
                    error_message = error_message + line
                return {
                    'result': 'RTE',
                    'error_message': error_message
                }
        if ret['result'] == CodeResult.CPU_TIME_ERROR or ret['result'] == CodeResult.REAL_TIME_ERROR:
            return {
                'result': 'TLE',
                'error_message': 'TimeLimitExceed',
                'time': kwargs['time_limit']/1000.00,
                'memory': ret['memory'] / (1000 * 1000)
            }
        else:
            if not self.checkFile(kwargs['stdout'], kwargs['factout']):
                return {
                    'result': 'Wrong Answer',
                    'error_message': None,
                    'time': ret['real_time'] / 1000.00,
                	'memory': ret['memory'] / (1000 * 1000)
                }
            return {
                'result': 'AC',
                'error_message': None,
                'time': ret['real_time'] / 1000,
                'memory': ret['memory'] / (1000 * 1000)
            }

    def checkRunnable(self,command):
        result = subprocess.Popen(command,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  )
        stdout, stderr = result.communicate(timeout=10)
        return str(stderr,encoding='utf-8')

    def checkFile(self,stdout, resultOut):
        with open(stdout, 'r', encoding='utf-8') as expectResult:
            std_lines = expectResult.readlines()
            std_lines_num = len(std_lines)
        with open(resultOut, 'r', encoding='utf-8') as factResult:
            fact_lines = factResult.readlines()
            fact_lines_num = len(fact_lines)
        if(fact_lines_num == 0):
        	return False;
        if ('\n' in std_lines[-1]):
            std_lines[-1] = std_lines[-1].rstrip('\n')
        if ('\n' in fact_lines[-1]):
            fact_lines[-1] = fact_lines[-1].rstrip('\n')
        if (fact_lines_num > std_lines_num or fact_lines_num < std_lines_num):
            return False
        for i in range(0, std_lines_num):
            if (std_lines[i] != fact_lines[i]):
                return False
            else:
                return True