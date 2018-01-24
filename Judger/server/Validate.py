import json
from server.config import lang_config

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
        if(not len(args['test_cases']) == 0):
            for test_case in args['test_cases']:
                if 'stdin' not in test_case or 'stdout' not in test_case:
                    return False

        if(args['lang'] not in lang_config):
            return False

        else:
            return True