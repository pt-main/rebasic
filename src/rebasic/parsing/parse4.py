from .base import Node
from .parsemeta import ParserMeta
# === start file ===
import re

class Parser4(ParserMeta):
    '''
# Parser4 (in alpha)
A regex-based parser that recognises syntactic constructs.
Each construct is defined by a (syntax_type, regex_pattern) pair.
The regex must match the entire input line (after line continuation handling)
and may contain named groups. The resulting AST node will have:

    type  = 'ast-node'
    value = syntax_type
    meta  = dictionary with all named groups from the match, plus
            guaranteed keys 'next', 'prev', 'val' (set to None if missing).

Usage:
```
patterns = [
    ('assign', r'(?P<var>\w+)\s*=\s*(?P<val>.+)'),
    ('print',  r'print\((?P<val>.+)\)')
]
parser = Parser4(patterns)
result = parser('x = 42\\nprint("hello")')
# result -> [
#   {'raw': 'x = 42', 'tokens': [Node(type='ast-node', value='assign',
#                         meta={'var': 'x', 'val': '42', 'next': None, 'prev': None})]},
#   {'raw': 'print("hello")', 'tokens': [Node(type='ast-node', value='print',
#                         meta={'val': '"hello"', 'next': None, 'prev': None})]}
# ]
```
    '''

    def __init__(self, patterns: list[tuple[str, str]]):
        '''
        Args:
        patterns: list[syntax_type, regex_pattern]
        '''
        self.patterns = [(name, re.compile(pat)) for name, pat in patterns]
        super().__init__()

    def reset(self):
        '''Reset internal state.'''
        self.tokens = []
        self.to_add = []

    def form(self, line: str) -> list[Node]:
        '''
        Match the (possibly multi-line) string against the defined patterns.
        Returns a list containing a single Node if a pattern matches.
        Raises ValueError if no pattern matches.
        '''
        for syntax_type, regex in self.patterns:
            m = regex.fullmatch(line)
            if m:
                # Extract all named groups
                meta = m.groupdict()
                # Ensure the three required keys exist
                for key in ('next', 'prev', 'val'):
                    if key not in meta:
                        meta[key] = None
                node = Node(type='ast-node', value=syntax_type, meta=meta)
                return [node]
        raise ValueError(f"Line does not match any pattern: {line}")

    def parse(self, string: str) -> list[dict[str, list[Node] | str]]:
        '''
        Parse a multi-line string, handling line continuation (lines ending with '\\').
        Returns a list of dictionaries with keys 'raw' and 'tokens'.
        '''
        for line in string.split('\n'):
            if line.strip() != '':
                self.to_add.append(line)
                if not line.endswith('\\'):
                    # Build the concatenated raw string
                    raw_lines = self.to_add
                    raw_line_final = ''
                    for i, raw_line in enumerate(raw_lines):
                        # Remove the trailing backslash that indicated continuation
                        raw_line_final += raw_line.rstrip('\\')
                        if i != len(raw_lines) - 1:
                            raw_line_final += '\n'
                    # Parse the accumulated block
                    tokens = self.form(raw_line_final)
                    self.eat(raw_line=raw_line_final, tokens=tokens)
                    self.to_add = []
        return self.tokens