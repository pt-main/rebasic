# === start file ===
class Repl:
    '''
    # Repl
    Simple repl for your languages. Support translators/interpreters (not compilers).
    '''
    class constants:
        TRANSLATOR = 0
        INTERPRETER = 1
    def __init__(
        self, 
        engine: 'Engine', 
        exit_cmd: str = 'exit-repr', 
        type: str = constants.INTERPRETER
    ) -> None:
        if type not in (
            self.constants.TRANSLATOR, 
            self.constants.INTERPRETER
        ):
            raise ValueError(f"Unknow type of repl: '{type}'")
        self.__type = type
        self._can_run = True
        self._exit = exit_cmd
        def off(*args): self._can_run = False
        engine.new_command(exit_cmd, off)
        self._engine = engine
    
    def run(self):
        if self.type == self.constants.INTERPRETER: self._run_interpreter()
        elif self.type == self.constants.TRANSLATOR: self._run_translator()
        else: raise ValueError(f"Unsupportable repl type: {self.constants}")

    def _start(self):
        text = f'Welcome to {self._engine.config._lang_name} repr (based on rebasic).'
        length = len(text)+5
        sep = '=' * length
        welcome = f"""{sep}\n{text.center(length)}\n{sep}"""
        print(welcome)
    
    def _run_interpreter(self):
        self._start()
        while self._can_run:
            try:
                while self._can_run:
                    code = input(f"\n{self._engine.config._lang_name} >>> ")
                    try: self._engine.compile(code)
                    except Exception as e: print(f"Error: {e}")
            except KeyboardInterrupt:
                print(f"KeyboardInterrupt. Type '{self._exit}' if you want exit.")

    def _run_translator(self):
        self._start()
        while self._can_run:
            try:
                while self._can_run:
                    code = input(f"\n{self._engine.config._lang_name} >>> ")
                    try:
                        result: str = str(self._engine.compile(code)); print('code :')
                        for line in result.strip().split('\n'): print(f"     : {line}")
                    except Exception as e: print(f"Error: {e}")
            except KeyboardInterrupt:
                print(f"KeyboardInterrupt. Type '{self._exit}' if you want exit.")