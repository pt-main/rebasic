# === start file ===
class Repl:
    def __init__(self, trs: 'Translator', exit_cmd: str = 'exit-repr'):
        self._can_run = True
        self._exit = exit_cmd
        def off(*args): self._can_run = False
        trs.new_command(exit_cmd, off)
        self._trs = trs

    def run(self):
        text = f'Welcome to {self._trs._lang_name} repr (based on rebasic).'
        length = len(text)+5
        sep = '=' * length
        welcome = f"""{sep}\n{text.center(length)}\n{sep}"""
        print(welcome)
        while self._can_run:
            try:
                while self._can_run:
                    code = input(f"\n{self._trs._lang_name} >>> ")
                    try:
                        result: str = str(self._trs.compile(code))
                        print('code :')
                        for line in result.strip().split('\n'):
                            print(f"     : {line}")
                    except Exception as e:
                        print(f"Error: {e}")
            except KeyboardInterrupt:
                print(f"KeyboardInterrupt. Type '{self._exit}' if you want exit.")