from rebasic import Engine
from rebasic.parsing import Node
from rebasic.systems.exceptions import RebasicRuntimeException

# one handler for different commands
def header(e: Engine, raw_line, tokens: list[Node]): 
    hcount = tokens[0].value.count('#')
    args = tokens[1].value
    e.context.add_to_code([
        f'<h{hcount}>{args}</h{hcount}>'
    ])

def create():
    e = Engine(std=False) # create engine without standart cmds
    def parser(raw_line: str, tokens: list): # custom parser
        try: e.work_default(raw_line, tokens)
        except RebasicRuntimeException: 
            e.context.add_to_code([raw_line])
    # set custom parser as default:
    e.md2html_parser = parser
    e._line_parser = 'md2html_parser'
    # register commands:
    e.new_command('#', header)
    e.new_command('##', header)
    e.new_command('###', header)
    e.new_command('####', header)
    return e


lang = create()
lang.compile('''
# md header
#### test md text
<p>text</p>
''')
code = lang.context.generate_code()
print(code)
with open('out.html', 'w') as f: f.write(code)