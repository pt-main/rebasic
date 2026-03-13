'''
# Rebasic Framework
An opensource project for create language translators/compilers/interpreters.

## Main Attributes
- `create_basic_lang()` func    - create rebasic with standart constructions:
    - `__sm [name]`                 - start macro
    - `__em`                        - end macro
    - `__cm [name]`                 - call macro
    - `__codeblock/ [name]`         - start code block
    - `/__codeblock`                - end code block
    - `__comptime [code block]`     - execute codeblock in python scope
    - `__rbimport [filename]`       - read & execute file on current lang
    - `# ...`                       - commentary
- `Engine` class                - main engine class
- `Parser` class                - universal parser (in format `command args, ...`)
- `Parser2` class               - universal parser with brackets (in format `command(args, ...)`)
- `Parser4` class   (alpha)     - best parser, regex based, full ast compleate. use so hard then with 1, 2, or 3 parser
    (`Parser4` or any other ast parser usage need full refactor of language)

## Main modules
- `langfile/`       : realization of json config for languages
- `parsing/`        : simple string parser for code
- `systems/`        : system classes and configs for rebasic
- `tooling/`        : tools and utils for languages
- `_basics`         : standarts for rebasic with std
- `engine`          : main class with rebasic translator

## Dev info
- Files can has comments like `#  === start file ===` . That's necessary for builder script.

---'''

__framework_meta__ = {
    'version': '1.7.2',
    'name': 'rebasic',
    'stage': 'alpha',
    'release': '1'
}

# === start file ===

from ._basics import basic_lang as create_basic_lang
from .engine import Engine
class parsing:
    from .parsing import (
        Parser, Parser2, Parser3, Parser4,
        Node, form_token_dict as _form_token_dict
    )
class tooling:
    from .tooling import (
        MetaGeneration, 
        Template, TemplateEngine,
        Repl,
        langtools,
    )