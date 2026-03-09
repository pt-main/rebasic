# <img width="3000" height="500" alt="rebasic-banner-gh" src="https://github.com/user-attachments/assets/e9c9c3bd-e3bb-43f1-a3f0-c8735e876989" />

[![Status](https://img.shields.io/badge/status-alpha-red.svg)](https://github.com/pt-main/rebasic)
[![GitHub](https://img.shields.io/github/v/tag/pt-main/rebasic.svg?label=GitHub)](https://github.com/pt-main/rebasic)
![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)
[![Language](https://img.shields.io/badge/main_language-python-yellow.svg)](https://github.com/pt-main/rebasic)
[![Python](https://img.shields.io/badge/require-python_3.10+-black.svg)](https://github.com/pt-main/rebasic)
[![Python](https://img.shields.io/badge/api-not_stable-red.svg)](https://github.com/pt-main/rebasic)
[![Dev](https://img.shields.io/badge/development-by_Pt-blue.svg)](https://github.com/pt-main/rebasic)

### `pip install rebasic`

Open-source project for creating programming languages.

# Features
Besides the main class, the framework includes:
- Parsing module: Includes standard syntax parsers and the `Node()` class – as a linear or AST node.
- Templating engine: Includes the `TemplateEngine()` and `Template()` classes, which allow building templates with support for default values. (Basic placeholder format in templates: `[[?placeholder_name]]`)
- Ready-to-use templating tools for generating code in different languages.
- Built-in `Repl()` class, which allows quickly creating REPLs for your languages.

The framework allows building compilers/interpreters/translators based on the main `Engine()` class, with full and flexible configuration of everything. The language engine supports an event system, logging, text/bytecode generation, and work with the pipeline system.

## Pipeline system operation
All code in rebasic is generated non-linearly. There is a dictionary of points, and code is added to each point separately and independently, and then at the end, during generation, the code is assembled into a single text (or a single byte stream). Here's an example:
```python
from rebasic import Engine

e = Engine()

with e.context.work_with_point('1') as ctx: # set current work point as 1
    ctx._add_tabs(1) # control tabs
    ctx.add_to_code(['test line 1', 'test line 2']) # add lines

with e.context.work_with_point('2') as ctx: 
    ctx._sub_tabs(1)
    ctx.add_to_code(['test line 3', 'test line 4']) 

with e.context.work_with_point('3') as ctx:
    ctx._add_tabs(2)
    ctx.add_to_code(['test line 5', 'test line 6'])

e.context.pipeline.set(['2', '1', '3']) # change pipeline
print(e.context.generate_code()) # generate code
''' ->
test line 3
test line 4

    test line 1
    test line 2

        test line 5
        test line 6
'''
```

# Language example
A simple Markdown dialect:
``` python
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
```

Or a simple interpreter:
``` python
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
    e.context._scope['hello_counter'] = 0 # create engine-scope variable
    # register commands:
    e.new_command('hello', hello) 
    e.new_command('count', count)
    return e


lang = create()
lang.compile('''
hello Pt
count
''')
```

# Connect
Copyright (c) 2026 Pt & Intelektika-team

SPDX-License-Identifier: Apache-2.0
