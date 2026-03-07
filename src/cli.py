from rebasic import Translator, create_basic_lang as basic_lang
__CliAvailable = True
# === start file ===
import os, platform, sys
CLI_NAME = 'rebasic'

class _RebasicCli:
    class Utils:
        @staticmethod
        def maxlen(data):
            out = []
            for i in data:
                out.append(len(str(i)))
            return max(out)
        @staticmethod
        def cls():
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')

    class color:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        
        BRIGHT_BLACK = '\033[90m'
        BRIGHT_RED = '\033[91m'
        BRIGHT_GREEN = '\033[92m'
        BRIGHT_YELLOW = '\033[93m'
        BRIGHT_BLUE = '\033[94m'
        BRIGHT_MAGENTA = '\033[95m'
        BRIGHT_CYAN = '\033[96m'
        BRIGHT_WHITE = '\033[97m'

        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

        @staticmethod
        def set(text, *col):
            data = col if isinstance(col, list) else [col]
            if isinstance(col, tuple):
                nd = []
                for i in col: nd.append(i)
                data = nd
            return f"{' '.join(data)}{text}{_RebasicCli.color.RESET}"




    class CliParser:
        def __init__(self) -> None:
            self.commands = {} # command:[handler, description, require_args, optional_args]
            self.add_command('help', self.help, 'Show this help message', [], [])
            self.debug = False
        
        def about(self):
            print(_RebasicCli.color.set('Rebasic - Opensource toolkit and framework', _RebasicCli.color.BLUE))
            print('Rebasic is a framework for create compilers, interpreters or translators.')
            print(f'Only {_RebasicCli.color.set('humanmade', _RebasicCli.color.YELLOW)}, by Pt')
            print('Licence', _RebasicCli.color.set('MIT', _RebasicCli.color.YELLOW))
            print()
        
        def help(self, *args):
            self.about()
            for cmd in self.commands.keys():
                print(f'{_RebasicCli.color.set('╭─────── Command ', _RebasicCli.color.GREEN)}[{_RebasicCli.color.set(cmd, _RebasicCli.color.YELLOW)}]')
                args = ''
                require_args = self.commands[cmd][2]
                for arg in require_args:
                    args += '<'+arg+'>'
                    if require_args.index(arg) != (len(require_args) - 1):
                        args += ' '
                print(_RebasicCli.color.set('⎬─ Args: ', _RebasicCli.color.GREEN) + _RebasicCli.color.set(args, _RebasicCli.color.BLUE))
                docs = self.commands[cmd][1].split('\n')
                print(_RebasicCli.color.set('⎬─ Desc:', _RebasicCli.color.GREEN))
                for line in docs:
                    print(_RebasicCli.color.set('│   ', _RebasicCli.color.GREEN) + line)
                print(_RebasicCli.color.set('╰───────', _RebasicCli.color.GREEN))
                print()
        
        def unknown(self, command):
            print(_RebasicCli.color.set('Unknown command: ', _RebasicCli.color.RED), end = '')
            print(_RebasicCli.color.set(f'[{command}]', _RebasicCli.color.BLUE))
            print(_RebasicCli.color.set(f'Type [{CLI_NAME} help] for help', _RebasicCli.color.YELLOW))
        
        def main(self):
            argv = sys.argv[1:]
            if len(argv) == 0:
                self.about()
                print(_RebasicCli.color.set('Type [help] for help', _RebasicCli.color.YELLOW))
                return
            if argv[0] == '--debug':
                argv = argv[1:]
                self.debug = True
            verbose = False
            if argv[0] == '--verbose':
                argv = argv[1:]
                verbose = True
            command = argv[0]
            args = argv[1:]
            def print_verbose(*args):
                if verbose: print(args)
            print_verbose(f"Command: {command}")
            print_verbose(f"Args: {args}")
            if command not in self.commands.keys():
                self.unknown(command)
                return
            require = self.commands[command][2]
            optional = self.commands[command][3]
            print_verbose(f"Require: {require}")
            print_verbose(f"Oprional: {optional}")
            if optional == []:
                if not (len(args) == len(require)):
                    print(_RebasicCli.color.set('Invalid argument length: ', _RebasicCli.color.RED)+str(len(args)))
                    print(f'(Reguire: {_RebasicCli.color.set(str(require), _RebasicCli.color.YELLOW)}[{len(require)
                    }], now: {len(args)})')
                    return
            else:
                if not (len(args) >= (len(require) + len(optional))):
                    print(_RebasicCli.color.set('Invalid argument length: ', _RebasicCli.color.RED)+str(len(args)))
                    print(
                        f'(Reguire: {_RebasicCli.color.set(str(require), _RebasicCli.color.YELLOW)
                        }[{len(require)}], {_RebasicCli.color.set(str(optional), _RebasicCli.color.YELLOW)
                        }[{len(optional)}], now: {len(args)})')
                    return
            try: 
                cmd = self.commands[command]
                print_verbose(cmd)
                print_verbose('calling: ')
                cmd[0](*args) # call handler
                print_verbose(*args)
            except Exception as e:
                print(_RebasicCli.color.set(f'Error: [{e}]', _RebasicCli.color.RED))
                if self.debug:
                    e.with_traceback()
                return

        def add_command(
            self, 
            cmd: str,
            handler: object, 
            description: str, 
            require_args: list[str], 
            optional_args: list[str] = []
        ):
            self.commands[cmd] = [handler, description, require_args, optional_args]


    def print_colored(*text: str, **kwargs):
        text = list(text)
        replaces = {
            '{RED}':_RebasicCli.color.RED,
            '{RESET}':_RebasicCli.color.RESET,
            '{GREEN}':_RebasicCli.color.GREEN,
            '{BLUE}':_RebasicCli.color.BLUE,
            '{BOLD}':_RebasicCli.color.BLUE,
        }
        for text_idx in range(len(text)):
            for key in replaces:
                text[text_idx] = text[text_idx].replace(key, replaces[key])
        print(*text, **kwargs)




    def execute(code: str):
        _RebasicCli.print_colored(f'Executing code: {{BLUE}}{{BOLD}}{code}{{RESET}}')
        try: basic_lang().compile(code)
        except Exception as e:
            _RebasicCli.print_colored(f"{{RED}}Execute Error:{{RESET}}\n{e}", )
            return
        _RebasicCli.print_colored('{GREEN}Executing compeate{RESET}')
    
    
    def run_pycode_in_scope(code: str):
        _RebasicCli.print_colored(f'Executing code: {{BLUE}}{{BOLD}}{code}{{RESET}}')
        __scope = {}
        for __key in locals():
            __scope[__key] = locals()[__key]
        for __key in globals():
            __scope[__key] = globals()[__key]
        try: exec(code, __scope, __scope)
        except Exception as e:
            _RebasicCli.print_colored(f"{{RED}}Execute Error:{{RESET}}\n{e}", )
            return
        _RebasicCli.print_colored('{GREEN}Executing compeate{RESET}')
    

    def open_and_run_pycode_in_scope(filename: str):
        _RebasicCli.print_colored(f'Opening: {{BLUE}}{{BOLD}}{filename}{{RESET}}')
        with open(filename, 'r') as f:
            code = f.read()
        _RebasicCli.print_colored(f'Executing code: {{BLUE}}{{BOLD}}{code}{{RESET}}')
        __scope = {}
        for __key in locals():
            __scope[__key] = locals()[__key]
        for __key in globals():
            __scope[__key] = globals()[__key]
        try: exec(code, __scope, __scope)
        except Exception as e:
            _RebasicCli.print_colored(f"{{RED}}Execute Error:{{RESET}}\n{e}", )
            return
        _RebasicCli.print_colored('{GREEN}Executing compeate{RESET}')





    def main():
        p = _RebasicCli.CliParser()
        commands = [
            (
                'execute', _RebasicCli.execute, 
                'Execute code on rebasic', 
                ['code'], []
            ),
            (
                'pycode', _RebasicCli.run_pycode_in_scope, 
                'Execute python code into rebasic framework', 
                ['code'], []
            ),
            (
                'opycode', _RebasicCli.open_and_run_pycode_in_scope,
                'Open python file and execute code into rebasic framework', 
                ['filename'], []
            ),
        ]
        for cmd in commands:
            p.add_command(*cmd)
        p.main()

if __CliAvailable:
    _RebasicCli.main()