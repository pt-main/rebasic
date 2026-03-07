from .engine import Engine, Parser

# === start file ===

def _create_runtime_scope(engine: Engine) -> dict[str, any]:
    '''
    ## _create_runtime_scope
    Create scope for executing python code in comptime.
    '''
    scope = locals()
    scope['ENGINE'] = engine
    scope['ADD_CMD'] = engine.new_command
    scope['GENERATE'] = engine.context.generate_code
    scope['COMPILE'] = engine.compile
    scope['PARSE'] = Parser()
    scope['CURR_POINT'] = engine.context.current_point
    scope['ADD_LINES'] = engine.context.add_to_code
    scope['_CODE'] = engine.context.code
    return scope

def _comptime(engine: Engine, args: str, *other):
    'comptime command realization'
    parsed = Parser()(args)[0]
    args: str = parsed['tokens'][1].value
    codeblock = args.strip()
    try: code = '\n'.join(engine.code_blocks[codeblock])
    except KeyError:
        raise RuntimeError(f'Unknnown codeblock: {codeblock}')
    scope = _create_runtime_scope(engine=engine)
    exec(code, scope, scope)


def _rbimport(self: Engine, raw: str, tokens):
    args = tokens[1].value
    with open(str(args), 'r') as f:
        content= f.read()
    self.compile(content)

def basic_lang(std_names: dict = {}) -> Engine:
    '''
    ## basic_lang
    Create language with std samples.

    Adding standart command and new:
    - `__comptime [codeblock_name]` - compile codeblock in python runtime
    - `__rbimport [filename]` - read & execute file on current translator

    (`std_names` keys: 'bct' for comptime, 'brbi' for rbimport)
    '''
    engine = Engine(std=True, std_names=std_names)
    def req(name: str, basic: str):
        if name in std_names: return std_names[name]
        else: return basic
    engine.new_command(
        req('bct', '__comptime'), 
        _comptime
    )
    engine.new_command(
        req('brbi', '__rbimport'), 
        _rbimport
    )
    return engine