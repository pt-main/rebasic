# === start file ===

class _Defaults:
    def _sm(self: 'Translator', raw: str, tokens):
        args = tokens[1].value
        self._in_macro.append(args)
    
    def _em(self: 'Translator', raw: str, tokens):
        if len(self._in_macro) > 0: name = self._in_macro.pop()
        else: raise RuntimeError(
            "Can't end macros while macros is not started."
        )
        self.macroses[name].pop()
    
    def _cm(self: 'Translator', raw: str, tokens):
        args = tokens[1].value
        try: code: str = '\n'.join(self.macroses[args.strip()])
        except KeyError:
            raise RuntimeError(f'Invalid macros name: {args}')
        self.compile(code=code, status='macros executing')
    
    def _cbs(self: 'Translator', raw: str, tokens):
        args = tokens[1].value
        codeblock_name = args.strip()
        self._write_raw = codeblock_name
        if codeblock_name not in self.code_blocks:
            self.code_blocks[codeblock_name] = []
            self.code_blocks[codeblock_name].append('')
    
    def _cbe(self: 'Translator', raw: str, tokens):
        self._write_raw = None