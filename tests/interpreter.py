from rebasic import Engine
from rebasic.parsing import Node

def hello(e: Engine, raw_line, tokens: list[Node]): # handler
    e.context._scope['hello_counter'] += 1
    val = tokens[1].value
    print(f'Hello, {val if val else 'World'}!')

def count(e: Engine, raw_line, tokens: list[Node]): # handler
    print(e.context._scope['hello_counter'])

def create():
    e = Engine(std=False) # create language without standart cmds
    e.context._scope['hello_counter'] = 0 # create engine-csope variable
    # register commands:
    e.new_command('hello', hello) 
    e.new_command('count', count)
    return e


lang = create()
lang.compile('''
hello Pt
hello Test
count 
''')