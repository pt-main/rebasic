from .translator import Translator, Parser

# === start file ===

def _create_runtime_scope(trs: Translator) -> dict[str, any]:
    '''
    ## _create_runtime_scope
    Create scope for executing python code in comptime.
    '''
    scope = locals()
    scope['TRS'] = trs
    scope['ADD_CMD'] = trs.new_command
    scope['GENERATE'] = trs.context.generate_code
    scope['COMPILE'] = trs.compile
    scope['PARSE'] = Parser()
    scope['CURR_POINT'] = trs.context.current_point
    scope['ADD_LINES'] = trs.context.add_to_code
    scope['_CODE'] = trs.context.code
    return scope

def _comptime(trs: Translator, args: str, *other):
    'comptime command realization'
    parsed = Parser()(args)[0]
    args: str = parsed['tokens'][1].value
    codeblock = args.strip()
    try: code = '\n'.join(trs.code_blocks[codeblock])
    except KeyError:
        raise RuntimeError(f'Unknnown codeblock: {codeblock}')
    scope = _create_runtime_scope(trs=trs)
    exec(code, scope, scope)


def _rbimport(self: Translator, raw: str, tokens):
    args = tokens[1].value
    with open(str(args), 'r') as f:
        content= f.read()
    self.compile(content)

def basic_lang(std_names: dict = {}):
    '''
    ## basic_lang
    Create language with std samples.

    Adding standart command and new:
    - `__comptime [codeblock_name]` - compile codeblock in python runtime
    - `__rbimport [filename]` - read & execute file on current translator

    (`std_names` keys: 'bct' for comptime, 'brbi' for rbimport)
    '''
    trs = Translator(std=True, std_names=std_names)
    def req(name: str, basic: str):
        if name in std_names: return std_names[name]
        else: return basic
    trs.new_command(
        req('bct', '__comptime'), 
        _comptime
    )
    trs.new_command(
        req('brbi', '__rbimport'), 
        _rbimport
    )
    return trs