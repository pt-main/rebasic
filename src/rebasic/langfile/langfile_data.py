# === start file ===
class LangfileData:
    '''
    # LangfileData
    Dataclass with values of langfile.
    '''
    lang_name: str = 'rebasic'
    lang_parser: str | None = None
    lang_code: str = ''
    lang_scope: dict[str, any] = {}
    lang_version: int = 0.1
    std_names = {
        'sm': '__sm',           # start macro
        'em': '__em',           # end macro
        'cm': '__cm',           # call macro
        'cbs': '__codeblock/',  # code block start
        'cbe': '/__codeblock',  # code block end
        'com': '#',             # commentary
    }
    std_include: bool = True
    _serialize_pipeline = [
        'lang_name', 
        'lang_version',
        'lang_code',
        'lang_scope',
        'std_names',
        'std_include',
    ]

    def create(self):
        dictionary = {}
        for attr in self._serialize_pipeline:
            dictionary[attr] = getattr(self, attr)
        return dictionary
    
    def load(self, dictionaty: dict[str, any]):
        for key in dictionaty:
            setattr(self, key, dictionaty[key])
        return self
    
    def __repr__(self):
        return str(self.create())