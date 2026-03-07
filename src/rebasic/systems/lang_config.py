# === start file ===

class _LangConfig:
    '''
    # LangConfig
    Language configurator class for rebasic.
    '''
    _lang_name: str = 'rebasic'
    _line_parser: str = 'work_std'
    _std_names: dict[str, str] = {
        'sm':     '__sm',           # start macro
        'em':     '__em',           # end macro
        'cm':     '__cm',           # call macro
        'cbs':    '__codeblock/',   # code block start
        'cbe':    '/__codeblock',   # code block end
        'com':    '#',              # commentary
    }