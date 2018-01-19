import copy
from model.C_CPP import C_CPP
from model.JAVA import JAVA

from server.config import lang_config
from model.PYTHON import PYTHON


class LanguageFactory:

    def __init__(self,language,outfile):
        self.language = language
        self.outfile = outfile

    def get_obj(self,**kwargs):
        my_config = copy.deepcopy(lang_config)
        if(self.language=='JAVA8'):
            obj = JAVA(my_config[self.language])
            obj.replace(self.outfile,kwargs['max_memory'])
            obj.to_list()
            return obj
        if(self.language=='C' or self.language=='CPP'):
            obj = C_CPP(my_config[self.language])
            obj.replace(self.outfile)
            obj.to_list()
            return obj
        if (self.language == 'PYTHON36' or self.language == 'PYTHON27'):
            obj = PYTHON(my_config[self.language])
            obj.replace(self.outfile)
            obj.to_list()
            return obj
