'''
# Rebasic Parser-v1
Default rebasic parser.
Format - 
'test\\\ncode' ->
[{'raw': 'test\\\ncode', 'tokens': [Node(type='command', value='test'), Node(type='args', value='code')]}]
'''


from .parsemeta import *

__TestAvailable = False

# === start file ===


class Parser(ParserMeta):
    '''
    # Parser
    Parse code to list of dictionaries.
    Parsing format: `command args`

    ## Example:
    Code:
    ```
    print(Parser()('test\\\ncode'))
    ```
    Output:
    ```
    [{'raw': 'test\\\ncode', 'tokens': [Node(type='command', value='test'), Node(type='args', value='code')]}]
    ```
    '''
    tokens: list[dict[str, list[Node] | str]]
    to_add: list

    def reset(self):
        self.tokens = []
        self.to_add = []
    
    def parse(self, string: str) -> list[dict[str, list[Node] | str]]:
        for line in string.split('\n'):
            if line.strip() != '':
                tokens = self.form(line.strip())
                raw_line = line
                self.to_add.append([raw_line, tokens])
                if not raw_line.endswith('\\'):
                    raw_line_final = ''
                    tokens_pre_final = []
                    index = 0
                    for raw_line, tokens in self.to_add:
                        raw_line_final += raw_line + (
                            '\n' if index != (len(self.to_add)-1) else ''
                        )
                        for token in tokens: 
                            if token.strip() != '': tokens_pre_final.append(token)
                        index += 1
                    tokens_final = [
                        Node(type='command', value=tokens_pre_final[0]),
                        Node(type='args', value=' '.join(tokens_pre_final[1:]))
                    ]
                    self.eat(raw_line=raw_line_final, tokens=tokens_final)
                    self.to_add = []
        return self.tokens
    
    def form(self, line: str) -> list[Node]:
        if line.endswith('\\'):
            line = line[:-1]
        if self.to_add == []:
            split = line.split(' ')
            command = split[0]
            command_len = len(command) + 1
            args = line[command_len:]
            return [command.strip(), args]
        else:
            return [line]
    

# === end file ===
if __TestAvailable:
    print(Parser()('test\\\ncode'))