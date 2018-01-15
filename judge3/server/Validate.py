import json
from language_config import  config

class Validate:
    def __init__(self,data):
        self.data = data

    def validateAgrs(self):
        args = self.data
        # args = json.loads(self.data)
        if(len(args) == 0 ):
            return False

        if('lang'not in args
                or'source_code' not in args
                or 'time_limit' not in args
                or 'memory_limit' not in args
                or 'test_cases' not in args):
            return False

        if(int(args['time_limit']) <= 0 or int(args['memory_limit']) <= 0):
            return False

        if(len(args['test_cases']) == 0):
            return False

        if(args['lang'] not in config):
            return False

        else:
            return True