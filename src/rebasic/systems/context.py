__TestAvailable = False
# === start file ===
class _LangContext:
    '''
    # LangContext
    Generation context class for rebasic
    '''
    class constants:
        TEXT_GEN_FORMAT = 0
        NUMERIC_GEN_FORMAT = 1
    
    def __init__(self):
        self.reset()

    def reset(self):
        self._scope: dict = {} # scope for modules talk
        self._add_comments: bool = False
        self._generation_format: int = self.constants.TEXT_GEN_FORMAT
        self._comment_start: str = '//'
        self._pipeline: list[str] = ['pre', 'main',]
        self.current_point: str = 'main'
        self.code: dict[str, dict[str, list[str | int | bytes] | str]] = {
            'pre': {'code':[], 'tabs':0},
            'main': {'code':[], 'tabs':0},
        }
    
    def work_with_point(ContextSelf, point: str):
        if not isinstance(point, str): raise TypeError('Type of [point] must be str')
        class _work_with_point:
            __cs: _LangContext
            _point: str
            _prev_point: str
            def __init__(self):
                self.__cs = ContextSelf
                self._point = point
            def  __enter__(self):
                self._prev_point = self.__cs.current_point
                self.__cs.current_point = self._point
                if self._point not in self.__cs.code:
                    self.__cs.code[self._point] = {'tabs': 0, 'code':[]}
                return self.__cs
            def __exit__(self, *args, **kwargs):
                self.__cs.current_point = self._prev_point
        return _work_with_point()

    @property
    def pipeline(ContextSelf):
        class _pipeline:
            __cs: _LangContext = ContextSelf
            def add(self, point: str) -> None:
                if not isinstance(point, str): raise TypeError('Type of [point] must be str')
                self.__cs._pipeline.append(point)
            def set(self, pipeline: list[str]) -> None:
                self.__cs._pipeline = pipeline
            def pop(self) -> None:
                self.__cs._pipeline.pop()
            def get(self) -> list[str]:
                return self.__cs._pipeline
        return _pipeline()

    def add_to_code(self, to_add: list[str | int | bytes]) -> None:
        if len(to_add) == 0: return
        value_type = type(to_add[0])
        for val in to_add: 
            if value_type != type(val):
                raise TypeError(
                    'Type of values in list [to_add] is different.'
                )
        allowed_types = (str,) if self._generation_format == self.constants.TEXT_GEN_FORMAT else (int, bytes)
        if value_type not in allowed_types:
            raise TypeError(f'Invalid type of data to add: {value_type}')
        if self.current_point in self.code:
            for add_point in to_add:
                if self._generation_format == self.constants.TEXT_GEN_FORMAT:
                    tabs = '    ' * self.code[self.current_point]['tabs']
                    to_append = tabs + add_point
                else: to_append = add_point
                self.code[self.current_point]['code'].append(to_append)
        else:
            self.code[self.current_point] = {}
            self.code[self.current_point]['tabs'] = 0
            self.code[self.current_point]['code'] = to_add

    def _add_tabs(self, idx: int = 1) -> None:
        if not isinstance(idx, int): raise TypeError('Type of [idx] must be int')
        self.code[self.current_point]['tabs'] += idx
    
    def _sub_tabs(self, idx: int = 1) -> None:
        if not isinstance(idx, int): raise TypeError('Type of [idx] must be int')
        self.code[self.current_point]['tabs'] -= idx

    def generate_code(self) -> str | list[int | bytes]:
        if self._generation_format == self.constants.TEXT_GEN_FORMAT:
            result = ''
            for point in self._pipeline:
                if self._add_comments: 
                    comment = f"{'=' * 30} {point} {'=' * 30}"
                    result += f"\n{self._comment_start} MARK:{point}\n{self._comment_start} {comment}\n"
                to_add = '\n'.join(self.code[point]['code']) 
                result += to_add + ('\n' * 2)
            return result
        elif self._generation_format == self.constants.NUMERIC_GEN_FORMAT:
            result = []
            for point in self._pipeline:
                to_add = self.code[point]['code']
                result.extend(to_add)
            return result
        else: raise ValueError(
            f'Unknown generation format: {self._generation_format}'
        )


# === end file ===
if __TestAvailable:
    lctx = _LangContext()
    lctx.pipeline.add('test')
    print(lctx.pipeline.get())
    # ['pre', 'main', 'test']