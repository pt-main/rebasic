from langfile_data import LangfileData
from rebasic import Translator, create_basic_lang
from rebasic._basics import _create_runtime_scope
__TestAvailable = True
# === start file ===
import os
import json





class Langfile:
    '''
    # Rebasic Langfile
    File format for create language only with one file.

    (Files `.jrlf` - Json Rebasic LangFile, or just `.json`)
    '''
    def create(self, filepath: str, data: LangfileData): 
        dictionary = data.create()
        with open(filepath, 'w') as f:
            json.dump(dictionary, f)
    
    def load(self, filepath: str):
        with open(filepath, 'r') as f:
            content = json.load(f)
        return LangfileData().load(content)
    
    def create_lang(self, data: LangfileData):
        trs = Translator(std=data.std_include)
        scope = _create_runtime_scope(trs)
        exec(data.lang_code, scope, scope)
        trs._lang_name = data.lang_name + "@" + str(data.lang_version)
        trs._std_names = data.std_names
        if data.lang_parser is not None:
            trs._line_parser = data.lang_parser
        trs.context._scope = data.lang_scope
        self.lang = trs
        return trs

    def pack_language_to_one_file(self, data: LangfileData):
        if '__BuildAvailable' not in globals().keys():
            raise SystemError(
                "[pack_language_to_one_file] function is not support inside framework build."
            )
        file_path = os.path.abspath(__file__)
        with open(file_path, 'r', encoding='utf-8') as f:
            framework_code = f.read()
        code = f'''
__slots__ = [
    'create_{data.lang_name}_language',
]


{framework_code}


def create_{data.lang_name}_language():
    data = LangfileData().load(
        dictionary={repr(data)},
    )
    trs = Translator(std=data.std_include)
    scope = _create_runtime_scope(trs)
    exec(data.lang_code, scope, scope)
    trs._lang_name = data.lang_name + "@" + str(data.lang_version)
    trs._std_names = data.std_names
    if data.lang_parser is not None:
        trs._line_parser = data.lang_parser
    trs.context._scope = data.lang_scope
    return trs
        '''
        return code

# === end file ===
if __TestAvailable:
    lf = Langfile()
    lfd = LangfileData()
    lfd.lang_name = 'test'
    lf.create_lang(lfd)