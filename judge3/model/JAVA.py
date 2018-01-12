
class JAVA:
    def __init__(self,config):
        self.exe_path = config['exe_path']
        self.max_memory = config['max_memory']
        self.source_name = config['source_name']
        self.complication = config['complication']
        self.compile_command =config['compile_command']
        self.run_args = config['run']['args']
        self.run_rule = config['run']['seccomp_rule']

    def replace(self,outfile,run_memory):
        self.compile_command = self.compile_command.format(exe_path = outfile)
        self.run_args = self.run_args.format(exe_path = outfile,max_memory = run_memory)

    def to_list(self):
        self.run_args =self.run_args.split(' ')
        self.compile_command = self.compile_command.split(' ')

    def getSourceName(self):
        return self.source_name

    def getComplication(self):
        return self.complication

    def getCompileCommand(self):
        return self.compile_command

    def getExe_path(self):
        return self.exe_path

    def getMax_memory(self):
        return self.max_memory

    def getRun_args(self):
        return self.run_args

    def getRun_rule(self):
        return self.run_rule

