import rebasic
from rebasic import Engine, Node


DEFAULT_POINT = 'default'
PRE_POINT = 'pre'
MAIN_POINT = 'main'



class BackendMeta:
    def configure(self, trs: Engine) -> Engine: 
        raise NotImplementedError()
    def next(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def prev(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def add(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def sub(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def out_current_int(self, trs: Engine, raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def out_current_char(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def input_to_current(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def set_point(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def go_to_point_if(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def go_to(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def syscall(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def include(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def jump(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def set(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def echo(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def swap(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()
    def copy(self, trs: Engine, mkvm: 'Mkvm', raw_line: str, tokens: list[Node]): 
        raise NotImplementedError()



class CppBack(BackendMeta):
    def __init__(self):
        self.names = []
        self.configured = False
    
    def configure(self, trs: Engine):
        if not self.configured:
            self.configured = True
            trs.context.pipeline.set([DEFAULT_POINT, PRE_POINT, 'head', MAIN_POINT, 'end'])
            with trs.context.work_with_point(point=DEFAULT_POINT) as ctx:
                ctx.add_to_code([self.default()])
            with trs.context.work_with_point(point='head') as ctx:
                ctx.add_to_code(['int main() {'])
            with trs.context.work_with_point(point='end') as ctx:
                ctx.add_to_code(['(void)(TAPE);', '}'])
        return trs


    def default(self):
        return """// mkvm
#include <iostream>
#include <vector>
int* TAPE = new int[262144]; // 262144 - 2^18
int POINTER = 0;
int STEP = 0;
typedef void(*SYSTEM_FUNCTYPE)();
std::vector<SYSTEM_FUNCTYPE> SYSTEMS;


template<typename T>
T input() {
    T value;
    while (true) {
        std::cin >> value;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\\n');
            std::cout << "Error: Input is incorrect.\\n";
        } else {
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\\n');
            return value;
        }
    }
}

int get_current_int() {return TAPE[POINTER];}
char get_current_char() {return (char) get_current_int();}
void next() {POINTER++;}
void prev() {POINTER--;}
void add() {TAPE[POINTER]++;}
void sub() {TAPE[POINTER]--;}
        """
    
    def _parse_one_arg(self, tokens: list[Node]):
        return tokens[1].value

    def next(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        args = 1 if (args.strip() == '') or (not args.isdigit()) else int(args)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            name = trs.gen._unique_name
            if args != 1: ctx.add_to_code([f'for (int {name}=0; {name}<{args}; {name}++) {{next();}}'])
            else: ctx.add_to_code([f'next();'])
    
    def prev(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        args = 1 if args.strip() == '' else int(args)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            name = trs.gen._unique_name
            if args != 1: ctx.add_to_code([f'for (int {name}=0; {name}<{args}; {name}++) {{prev();}}'])
            else: ctx.add_to_code([f'prev();'])
    
    def add(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        args = 1 if args.strip() == '' else int(args)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            name = trs.gen._unique_name
            if args != 1: ctx.add_to_code([f'for (int {name}=0; {name}<{args}; {name}++) {{add();}}'])
            else: ctx.add_to_code([f'add();'])
    
    def sub(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        args = 1 if args.strip() == '' else int(args)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            name = trs.gen._unique_name
            if args != 1: ctx.add_to_code([f'for (int {name}=0; {name}<{args}; {name}++) {{sub();}}'])
            else: ctx.add_to_code([f'sub();'])

    
    def out_current(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code(['std::cout << get_current_char();'])
    
    def out_current_int(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code(['std::cout << get_current_int();'])
    
    def input_to_current(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code(['TAPE[POINTER] = input<int>();'])
    
    def set_point(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens))
        name = trs.gen._unique_name if args.strip() == '' else args 
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'{name}:'])
            self.names.append(name)
    
    def go_to_point_if(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens)).split(' ')
        if len(args) != 3: raise ValueError
        name = args[2]
        oper = args[0]
        value = args[1]
        name = self.names.pop() if name.strip() == '' else name
        for char in oper: 
            if char not in ('=', '!', '>', '<'): raise ValueErrors
        if len(oper) != 2 :
            if oper not in ('>', '<'): raise ValueError
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'if (get_current_int() {oper} {value}){{goto {name};}}'])
    
    def go_to(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens))
        name = self.names.pop() if args.strip() == '' else args
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'goto {name};'])
    
    def syscall(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'SYSTEMS[TAPE[0]]();'])
    
    def include(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens))
        if args.strip() == '':
            raise ValueError('File not found')
        with open(f'{args}.cpp', 'r') as f:
            content = f.read()
        with trs.context.work_with_point(point=PRE_POINT) as ctx:
            ctx.add_to_code([content])
    
    def set(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'TAPE[POINTER] = {args};'])
    
    def jump(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        args = 1 if args.strip() == '' else int(args)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'POINTER = {args};'])
    
    def echo(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = self._parse_one_arg(tokens)
        text = list(repr(args).replace("'''", '"""').replace('\\\\', '\\'))
        text[0] = '"'
        text[-1] = '"'
        text = ''.join(text)
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([f'std::cout << {text};'])
    
    def swap(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens)).split(' ')
        if len(args) != 2: raise ValueError
        sec1 = int(args[0])
        sec2 = int(args[1])
        temp1 = trs.gen._unique_name
        temp2 = trs.gen._unique_name
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([
                f"int {temp1}_temp = TAPE[{sec1}];",
                f"int {temp2}_temp = TAPE[{sec2}];",
                f"TAPE[{sec1}] = {temp2}_temp;",
                f"TAPE[{sec2}] = {temp1}_temp;",
            ])
    
    def copy(self, trs: Engine, mkvm: 'Mkvm', raw_line, tokens: list[Node]):
        args = str(self._parse_one_arg(tokens)).split(' ')
        if len(args) != 2: raise ValueError
        sec1 = args[0]
        sec2 = args[1]
        with trs.context.work_with_point(point=MAIN_POINT) as ctx:
            ctx.add_to_code([
                f"TAPE[{sec2}] = TAPE[{sec1}];",
            ])


class Mkvm:
    def __init__(self, backend: type[BackendMeta] = CppBack):
        self._trs = Engine(std=True, std_names={
            'sm':'@func', 
            'em':'@end', 
            'cm':'@call',
            'cbs':'',
            'cbe':'',
            'com':';',
        })
        self._debug = 0
        self._trs.event.add_handler(
            self._trs.constants.events.COMPILE_LINE_START_EVENT,
            lambda trs, ses: (
                trs.context.add_to_code(
                    ['STEP += 1;', 
                    ('std::cout << "/" << STEP << "/\\n";') 
                    if self._debug else '']
                    )
                ) 
        )
        self._trs.context._add_comments = True
        self._trs.context._comment_start = '//'
        self._back = backend()
        self._reg_all()
        self._trs._lang_name = 'mkvm'
    
    def compile(self, code: str):
        self._trs.compile(code)
        return self.gen_code()
    
    def gen_code(self):
        self._trs = self._back.configure(self._trs)
        return self._trs.context.generate_code()
    
    def _reg_all(self):
        def default_handler(function):
            def command(trs: Engine, raw_line: str, tokens: list[Node]):
                function(trs, self, raw_line, tokens)
            return command
        def reg(function, cmd_name):
            self._trs.new_command(
                cmd_name, 
                default_handler(function)
            )
        reg(self._back.next, 'next')             
        reg(self._back.prev, 'prev')             
        reg(self._back.add, 'add')              
        reg(self._back.sub, 'sub')              
        reg(self._back.input_to_current, 'in') 
        reg(self._back.out_current_char, 'outc')      
        reg(self._back.out_current_int, 'outi')  
        reg(self._back.set_point, 'point')
        reg(self._back.go_to_point_if, 'gotoif') 
        reg(self._back.go_to, 'goto') 
        reg(self._back.syscall, 'syscall')   
        reg(self._back.include, 'incude') 
        reg(self._back.set, 'set')      
        reg(self._back.jump, 'jump')
        reg(self._back.echo, 'echo')
        reg(self._back.swap, 'swap')
        reg(self._back.copy, 'copy')



if __name__ == '__main__':
    code =  """
point start
    add
    copy POINTER POINTER+1
    next
    outi
    echo -
gotoif != 100 start
    """
    with open('a.cpp', 'w') as f:
        f.write(Mkvm().compile(code))