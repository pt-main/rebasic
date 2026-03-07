'''
# Rebasic Parser-v2
Default rebasic parser.
'''


from parsemeta import *

__TestAvailable = False

# === start file ===


class Parser2(ParserMeta):
    '''
    # Parser v2
    Parse code to list of dictionaries.
    Parsing format: `command(args)`

    ## Example:
    Code:
    ```
    print(Parser2()('test\\\n(\ncode\n)'))
    ```
    Output:
    ```
    [{'raw': 'test\\\n(\ncode\n)', 'tokens': [Node(type='command', value='test'), Node(type='args', value='code')]}]
    ```
    '''
    tokens: list[dict[str, list[Node] | str]]
    to_add: list

    def reset(self):
        self.tokens = []
        self.to_add = []
    
    def parse(self, string: str) -> list[dict[str, list[Node] | str]]:
        string_split = string.split('\n')
        line_idx = 0
        for line in string_split:
            if line.strip() != '':
                tokens = self.form(line.strip())
                raw_line = line
                self.to_add.append([raw_line, tokens])
                try: next_line = string_split[line_idx + 1]
                except: next_line = ''
                if not raw_line.endswith(('\\', '(')) and next_line.strip() != ')':
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
                    cmdtoken = Node(type='command', value=tokens_pre_final[0])
                    argstoken = Node(type='args', value=''.join(tokens_pre_final[1:]))
                    if not (
                        (argstoken.value.strip()).startswith('(') 
                        and (argstoken.value.strip()).endswith(')') 
                    ):
                        raise ValueError(
                            f'Parsing Error: Brackets is not found. Do you forgot format?\nArgs: {argstoken.value}'
                        )
                    argstoken.value = argstoken.value.strip()[1:-1]
                    tokens_final = [
                        cmdtoken, 
                        argstoken
                    ]
                    self.eat(raw_line=raw_line_final, tokens=tokens_final)
                    self.to_add = []
            line_idx += 1
        return self.tokens
    
    def form(self, line: str) -> list[Node]:
        if line.endswith('\\'):
            line = line[:-1]
        if self.to_add == []:
            to_add_pre = ''
            if line.endswith('('): to_add_pre = '('
            elif line.strip().endswith(')'): to_add_pre = '('
            split = line.split('(')
            command = split[0]
            command_len = len(command) + 1
            args = to_add_pre + line[command_len:]
            return [command.strip(), args]
        else:
            return [line]
    

# === end file ===
if __TestAvailable:
    print(Parser2()('test() \\\nbar(2)\n)\ntest()'))