# === start file ===

class _Defaults:
    def _sm(self: 'Engine', raw: str, tokens):
        args = tokens[1].value
        self._in_macro.append(args)
    
    def _em(self: 'Engine', raw: str, tokens):
        if len(self._in_macro) > 0: name = self._in_macro.pop()
        else: raise RuntimeError(
            "Can't end macros while macros is not started."
        )
        self.code_state.macroses[name].pop()
    
    def _cm(self: 'Engine', raw: str, tokens):
        args = tokens[1].value
        try: code: str = '\n'.join(self.code_state.macroses[args.strip()])
        except KeyError:
            raise RuntimeError(f'Invalid macros name: {args}')
        self.compile(code=code, status='macros executing')
    
    def _cbs(self: 'Engine', raw: str, tokens):
        args = tokens[1].value
        codeblock_name = args.strip()
        self._write_raw = codeblock_name
        if codeblock_name not in self.code_state.code_blocks:
            self.code_state.code_blocks[codeblock_name] = ['']
    
    def _cbe(self: 'Engine', raw: str, tokens):
        self._write_raw = None