from rebasic import Engine
from rebasic.parsing import Node, Parser, Parser4
from rebasic.systems.exceptions import RebasicRuntimeException

def header(e: Engine, raw_line: str, tokens: list[Node]): 
    token = tokens[0]
    hcount = token['header'].count('#')
    if token['header'] != '#' * hcount: raise ValueError(f"Invalid head: '{raw_line}'")
    args: str = token['text']
    e.context.add_to_code([f'<h{hcount}>{args}</h{hcount}>'])

def bold(e: Engine, raw_line, tokens: list[Node]): 
    args = tokens[1].value
    e.context.add_to_code([f'<p style="font-weight: bold;">{args}</p>'])

def cursive(e: Engine, raw_line, tokens: list[Node]): 
    args = tokens[1].value
    e.context.add_to_code([f'<p style="font-style: italic;">{args}</p>'])

def styled(e: Engine, raw_line, tokens: list[Node]): 
    args = tokens[1].value
    parsed = Parser()(args)[0]['tokens']
    style = parsed[0].value
    text = parsed[1].value
    e.context.add_to_code([f'<p style="{style}">{text}</p>'])

def create():
    engine = Engine(std=True, std_names={
        'sm':'', 'cm':'', 'em':'@end',
        'cbs':'', 'cbe':'',
    })
    parser = Parser4([
        ('header', r'!(\s*)+(?P<header>#+)(\s*)+(?P<text>.+)'),
    ])
    engine.md2html_parser = parser
    engine._line_parser = 'md2html_parser'
    
    engine.new_command('header', header)
    engine.new_command('style', bold)
    return engine

result = create().compile('''
!## test
''')

with open('out.html', 'w') as f: f.write(result)


parser = Parser4([
    ('header', r'!(\s*)+(?P<header>#+)(\s*)+(?P<text>.+)'),
])
print(parser('!### test text\n!# test'))