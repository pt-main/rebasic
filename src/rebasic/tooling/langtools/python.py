from rebasic.tooling import Template, TemplateEngine
from .__templates import _Templates
from ._backend_template import _TextBackend
# === start file ===




class PythonTool(_TextBackend):
    __ts = _Templates()
    func_template = Template(__ts._python_func_template, args="*", returntype="any")
    class_template = Template(__ts._python_class_template, metaclasses="")
    
    def add_tabs(
        self, 
        string: str, 
        tabs_conunt: int = 1,
        spaces_in_tab: int = 4,
    ) -> str:
        if not isinstance(string, str): raise TypeError('Type of [string] must be str')
        if not isinstance(tabs_conunt, int): raise TypeError('Type of [tabs_count] must be int')
        if not isinstance(spaces_in_tab, int): raise TypeError('Type of [spaces_int_tab] must be int')
        lines = string.split('\n')
        result = []
        for line in lines:
            tabs = (' ' * spaces_in_tab) * tabs_conunt
            result.append(tabs + line)
        string = '\n'.join(result)
        del lines, result
        return string
    
    def create_class(
        self,
        name: str,
        *,
        body: str = '...',
        metaclasses: list[str] = [],
        docs: str = 'class has no documentation',
        add_tabs: int = 0,
        **kwargs,
    ):
        if not isinstance(name, str): raise TypeError('Type of [name] must be str')
        if not isinstance(body, str): raise TypeError('Type of [body] must be str')
        if not isinstance(metaclasses, list): raise TypeError('Type of [metaclasses] must be list')
        if not isinstance(docs, str): raise TypeError('Type of [docs] must be str')
        if not isinstance(add_tabs, int): raise TypeError('Type of [add_tabs] must be int')
        metaclasses = ', '.join(metaclasses)
        body = self.add_tabs(body)
        code = self.class_template.work(
            classname=name,
            classbody=body, 
            classdocs=docs,
            metaclasses=metaclasses,
        )
        result = self.add_tabs(code, add_tabs)
        del code, metaclasses, body, code
        return result
    
    def create_func(
        self, 
        name: str, 
        *,
        body: str = "...",
        args: dict = {'*':''},
        return_type: str = "any",
        add_tabs: int = 0,
        docs: str = 'function has no documentation',
    ):
        if not isinstance(name, str): raise TypeError('Type of [name] must be str')
        if not isinstance(body, str): raise TypeError('Type of [body] must be str')
        if not isinstance(args, dict): raise TypeError('Type of [args] must be str')
        if not isinstance(return_type, str): raise TypeError('Type of [return_type] must be str')
        if not isinstance(add_tabs, int): raise TypeError('Type of [add_tabs] must be int')
        if not isinstance(docs, str): raise TypeError('Type of [docs] must be str')
        funcargs = []
        for arg in args:
            val = args[arg]
            if val == '': funcargs.append(f'{arg}')
            else: funcargs.append(f"{arg} = {val}")
        funcargs = ', '.join(funcargs)
        body = self.add_tabs(body)
        code = self.func_template.work(
            funcname=name,
            funcdocs=repr(str(docs)),
            funcbody=body,
            args=funcargs,
            returntype=return_type,
        )
        result = self.add_tabs(code, add_tabs)
        del funcargs, body, code
        return result