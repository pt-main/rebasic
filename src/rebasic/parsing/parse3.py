from .base import Node
from .parsemeta import ParserMeta
__TestAvailable = True
# === start file ===

class Parser3(ParserMeta):
    '''
    # Parser v3 (in beta)

    Support:
    - `command args`
    - `command(args)`
    - `command { ... }`
    '''
    def reset(self):
        self.tokens = []         
        self.current_raw = []    
        self.current_command = None 
        self.brace_level = 0        
        self.in_block = False       

    def parse(self, string: str) -> list[dict]:
        lines = string.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if not self.in_block:
                if not line.strip():
                    i += 1
                    continue
                if '{' in line:
                    cmd_part, _ = line.split('{', 1)
                    self.current_command = cmd_part.strip()
                    self.current_raw = [line]
                    self.brace_level = line.count('{') - line.count('}')
                    self.in_block = True
                    if self.brace_level == 0:
                        self._finalize_block()
                else:
                    token = self._parse_simple_line(line)
                    if token:
                        self.tokens.append(token)
                i += 1
            else:
                self.current_raw.append(line)
                self.brace_level += line.count('{') - line.count('}')
                if self.brace_level == 0:
                    self._finalize_block()
                i += 1
        return self.tokens

    def _finalize_block(self):
        full_raw = '\n'.join(self.current_raw)
        first = full_raw.find('{')
        last = full_raw.rfind('}')
        if first != -1 and last != -1 and last > first:
            body = full_raw[first+1:last].strip()
        else:
            body = ''
        tokens = [
            Node(type='command', value=self.current_command),
            Node(type='args', value=body)
        ]
        self.tokens.append({'raw': full_raw, 'tokens': tokens})
        self.in_block = False
        self.current_command = None
        self.current_raw = []
        self.brace_level = 0

    def _parse_simple_line(self, line: str) -> dict | None:
        '''Разбор строки без фигурных скобок (command args или command(args)).'''
        line = line.strip()
        if not line:
            return None
        if '(' in line:
            parts = line.split('(', 1)
            command = parts[0].strip()
            rest = parts[1]
            if rest.endswith(')'):
                args = rest[:-1].strip()
            else:
                last_close = rest.rfind(')')
                if last_close != -1:
                    args = rest[:last_close].strip()
                else:
                    args = rest.strip()
        else:
            parts = line.split(' ', 1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ''
        tokens = [
            Node(type='command', value=command),
            Node(type='args', value=args)
        ]
        return {'raw': line, 'tokens': tokens}