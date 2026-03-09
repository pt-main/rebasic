from .systems.context import _LangContext
from .parsing import Parser, Parser2
from .systems.exceptions import (
    RebasicException, 
    RebasicRuntimeException, 
    RebasicSystemException,
    RebasicError,
)
from .systems.state import _LangState
from .systems.code_state import _CodeState
from .systems.lang_config import _LangConfig
from .systems.generation import _LangGenerator
from .systems.event import _EventSystem
from ._defaults import _Defaults


# === start file ===



# ===================================
#       MARK: ENGINE CLASS
# ===================================
class Engine:
    '''
    # Engine
    Rebasic - an opensource project with sample for any
    compilers/translators/interpreters.

    ## Methods
    - `compile(code)`                      - compile code
    - `context.generate_code()`                    - generate compiled code
    - `new_command(cmd_name, cmd_parser)`  - add new command
    - `work_[type](raw_line, tokens)`             - compile one line
    '''
    class constants:
        class events:
            def __init__(self):
                self.__curr = 0
                self.events = []
                def __gen_next():
                    self.__curr += 1
                    self.events.append(self.__curr)
                    return self.__curr
                # compile events
                self.COMPILE_START_EVENT = __gen_next()
                self.COMPILE_END_EVENT = __gen_next()
                self.COMPILE_LINE_START_EVENT = __gen_next()
                self.COMPILE_LINE_END_EVENT = __gen_next()
                self.COMPILE_SYSTEM_EXCEPTION_EVENT = __gen_next()
                self.COMPILE_RUNTIME_EXCEPTION_EVENT = __gen_next()
                self.COMPILE_EXCEPTION_EVENT = __gen_next()
                # work default events
                self.WORK_DEFAULT_START_EVENT = __gen_next()
                self.WORK_DEFAULT_END_EVENT = __gen_next()
                # work std events
                self.WORK_STD_START_EVENT = __gen_next()
                self.WORK_STD_END_EVENT = __gen_next()
                self.WORK_STD_ADD_TO_MACRO_EVENT = __gen_next()
                self.WORK_STD_ADD_TO_CODEBLOCK_EVENT = __gen_next()
                self.WORK_STD_WRITE_SYSTEM_EVENT = __gen_next()
                self.WORK_STD_EXEC_SYS_CMD_EVENT = __gen_next()
                self.WORK_STD_EXEC_CMD_EVENT = __gen_next()
                # initialization & other events
                self.INITIALIZATION_START_EVENT = __gen_next()
                self.INITIALIZATION_END_EVENT = __gen_next()
                self.RESET_START_EVENT = __gen_next()
                self.RESET_END_EVENT = __gen_next()


    def __init__(
        self, 
        std: bool = False, 
        backend_tool: object = lambda *args: None,
        std_names: dict = {},
    ) -> None:
        if not isinstance(std, bool): raise TypeError('Type of [std] must be bool')
        self.__backend__: int = 0
        self.backend: object | None = backend_tool(self)
        self.constants.events = self.constants.events()
        self.reset()
        self.event.call_event(self.constants.events.INITIALIZATION_START_EVENT)
        self.state._log(f'initialize class', 'info')
        self.__std_cmd = std
        for key in std_names: self.config._std_names[key] = std_names[key]
        if std: self._reg_std() # add standart commands
        self.config._line_parser = 'work_' + ('std' if std else 'default')
        self.state._log(f'class initialization successful', 'info')
        self.event.call_event(self.constants.events.INITIALIZATION_END_EVENT)
        self._documentation_available = []
    
    def _reg_std(self):
        parser = Parser()
        self.new_command(self.config._std_names['sm'], _Defaults._sm, parser)
        self.new_command(self.config._std_names['em'], _Defaults._em, parser)
        self.new_command(self.config._std_names['cm'], _Defaults._cm, parser)
        self.new_command(self.config._std_names['cbs'], _Defaults._cbs, parser)
        self.new_command(self.config._std_names['cbe'], _Defaults._cbe, parser)
    
    def reset(self):
        super().__init__()
        self.event = _EventSystem(engine=self)
        for event in self.constants.events.events: self.event.add_event(event)
        self.event.call_event(self.constants.events.RESET_START_EVENT)
        self.context = _LangContext()
        self.parser = Parser()
        self.code_state = _CodeState()
        self.config = _LangConfig()
        self.state = _LangState()
        self.gen = _LangGenerator()
        self.__std_cmd: bool = False
        self._write_raw: str | None = None
        self._write_raw_system: str | None = None
        self._in_macro: list[str] = []
        # commands: dict[
        #   command: 
        #       handler     : [callable(engine, args, rawline)], 
        #       args_parser : [callable(raw_line)],
        #       docs        : [string]
        # ]
        self.commands: dict[str, dict[str, object]] = {}
        self.event.call_event(self.constants.events.RESET_END_EVENT)
    
    def new_command(
        self, 
        command_name: str, 
        handler: object,
        args_parser: object = Parser(),
        docstring: str = 'command has no docs'
    ) -> None:
        if not isinstance(command_name, str): raise TypeError('Type of [command_name] must be str')
        self.state._log(f'added command: {command_name}', 'info')
        self.commands[command_name] = {'h':handler, 'ap':args_parser, 'd':docstring}

    # ===================================
    #           MARK: COMPILE
    # ===================================
    def compile(
        self, 
        code: str, 
        status: str = 'executing code'
    ) -> str:
        self.state._log(f'compilation start with status: {status}', 'info') 
        self.context._scope['_code'] = code
        self.event.call_event(self.constants.events.COMPILE_START_EVENT)
        parsed = self.parser(code)
        line_index = 0
        for line in parsed:
            self.state._log(f'compiling line: {repr(line['raw'])}', 'info') 
            self.event.call_event(self.constants.events.COMPILE_LINE_START_EVENT)
            try: 
                args = (line['raw'], line['tokens'])
                parse_line = getattr(self, self.config._line_parser)
                parse_line(*args)
            except (RebasicSystemException, SystemError) as e:
                self.event.call_event(self.constants.events.COMPILE_SYSTEM_EXCEPTION_EVENT)
                self.state._log(f'compilation system error: {e}', 'error')
                raise SystemError(f'System error at [{status}]:\n    {e}')
            except (RebasicRuntimeException, SyntaxError, RuntimeError) as e:
                self.event.call_event(self.constants.events.COMPILE_RUNTIME_EXCEPTION_EVENT)
                self.state._log(f'compilation runtime error: {e}', 'error')
                raise RebasicError(
                    err=str(e), 
                    line=line['raw'], 
                    index=line_index, 
                    action=status,
                    naming=f'Runtime Error => {self.config._lang_name}'
                )
            except (RebasicException, RebasicError) as e:
                self.event.call_event(self.constants.events.COMPILE_EXCEPTION_EVENT)
                self.state._log(f'compilation error: {e}', 'error')
                raise RebasicError(
                    err=str(e), 
                    line=line['raw'], 
                    index=line_index, 
                    action=status,
                    naming=f'Error => {self.config._lang_name}'
                )
            self.event.call_event(self.constants.events.COMPILE_LINE_END_EVENT)
            line_index += 1
        self.event.call_event(self.constants.events.COMPILE_END_EVENT)
        return self.context.generate_code()

    def work_default(self, raw_line: str, tokens: list) -> None:
        self.state._log(f'start default work on line: {raw_line}', 'info')
        self.context._scope['_work_line'] = raw_line
        self.event.call_event(self.constants.events.WORK_DEFAULT_START_EVENT)
        command: str = tokens[0].value
        if '(' in command:
            command = command.split('(')[0]
        if self.state.DEBUG_MODE: print(f'------> {command} (default mode)')
        if self.state.DEBUG_MODE: print('executing:', repr(raw_line), tokens, repr(command))
        if self.state.DEBUG_MODE: print('commands:', self.commands)
        if self.context._add_comments: 
            self.context.add_to_code([f"{self.context._comment_start
            } Executing command: {command}"])
        status = True
        if command in self.commands.keys():
            cmd = self.commands[command]
            parsed = cmd['ap'](raw_line)[0]
            tokens = parsed['tokens']
            cmd['h'](self, raw_line, tokens)
        else: status = False
        self.event.call_event(self.constants.events.WORK_DEFAULT_END_EVENT)
        self.state._log(f'end default work on line: {raw_line}, success: {status}', 'info')
        if self.__std_cmd: return status
        else:
            if not status:
                raise RebasicRuntimeException(f'Unknown Syntax: {command}')
    
    def work_std(self, raw_line: str, tokens: list) -> None:
        self.state._log(f'start work on line: {raw_line}', 'info')
        self.event.call_event(self.constants.events.WORK_DEFAULT_START_EVENT)
        command: str = tokens[0].value
        # ===================================
        #        MARK: BASIC LOGICS
        # ===================================
        if self.context._add_comments: 
            self.context.add_to_code([f"{self.context._comment_start
            } Executing {repr(raw_line)}"])
        if (self._in_macro != []):
            self.event.call_event(self.constants.events.WORK_STD_ADD_TO_MACRO_EVENT)
            self.state._log(f'add line to macros: {raw_line}', 'info')
            for macro_name in self._in_macro:
                self.state._log(f'state: in macro {self._in_macro
                }, macro name {macro_name}', 'info')
                if self.context._add_comments: 
                    self.context.add_to_code([f"{self.context._comment_start
                    } Add code to macros {macro_name}"])
                if macro_name in self.code_state.macroses and command: 
                    self.code_state.macroses[macro_name].append(raw_line)
                else: self.code_state.macroses[macro_name] = [raw_line]
            if command.strip() not in (self.config._std_names['sm'], self.config._std_names['em']):
                return
        elif (self._write_raw is not None) and (raw_line.strip() != self.config._std_names['cbe']):
            self.event.call_event(self.constants.events.WORK_STD_ADD_TO_CODEBLOCK_EVENT)
            codeblock_name = self._write_raw
            if self.context._add_comments: 
                self.context.add_to_code([f"{self.context._comment_start
                } Add code to codeblock {codeblock_name}"])
            if codeblock_name in self.code_state.code_blocks:
                self.code_state.code_blocks[codeblock_name].append(raw_line)
            else: self.code_state.code_blocks[codeblock_name] = [raw_line]
            return
        elif (self._write_raw_system is not None):
            self.event.call_event(self.constants.events.WORK_STD_WRITE_SYSTEM_EVENT)
            codeblock_name = self._write_raw_system
            if self.context._add_comments: 
                self.context.add_to_code([f"{self.context._comment_start
                } Add code to codeblock {codeblock_name}"])
            if codeblock_name in self.code_state.code_blocks:
                self.code_state.code_blocks[codeblock_name].append(raw_line)
            else: self.code_state.code_blocks[codeblock_name] = [raw_line]
            return
        if self.state.DEBUG_MODE: print(f'------> {command} (std mode)')
        if self.state.DEBUG_MODE: print('executing:', repr(raw_line), tokens)
        if self.state.DEBUG_MODE: print(
            'state:', repr(self._write_raw), 
            repr(self.config._std_names), 
            self._in_macro, 
        )
        self.event.call_event(self.constants.events.WORK_STD_EXEC_CMD_EVENT)
        if self.work_default(raw_line, tokens): pass
        elif raw_line.strip().startswith(self.config._std_names['com']): 
            self.context.add_to_code([f'{self.context._comment_start}{raw_line.strip()[1:]}'])
        else: raise RebasicRuntimeException(f'Unknown Syntax: {command}')
        self.event.call_event(self.constants.events.WORK_DEFAULT_END_EVENT)
        self.state._log(f'start work on line: {raw_line}', 'info')
        return True