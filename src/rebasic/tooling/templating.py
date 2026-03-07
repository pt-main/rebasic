__TestAvailable = False
# === start file ===

class Template:
    '''
    # Template 
    Class with info about template. 

    ### Extends: 
        - `template` - template text with placeholders
        - `defaults` - default values for template
    '''
    def __init__(self, template: str, **defaults: str) -> None:
        if not isinstance(template, str):
            raise TypeError(
                'Invalid input type: Tepmlate must be type str.'
            )
        for key in defaults:
            if not isinstance(defaults[key], str) and key != '__dict':
                err = f'Invalid input type: Defaults keys must be type str \
(now: {type(defaults[key])}). Warning skipped, type converted.'
                print(err)
                defaults[key] = str(defaults[key])
        self.template = template
        self.defaults = defaults
    
    def work(self, **kwargs) -> str:
        return work_template(self, **kwargs)
    
    def __repr__(self) -> str:
        return self.template

class TemplateEngine:
    '''
    # TemplateEngine
    Templating engine for rebasic framework. 
    Default placeholder format: `[[?placeholder_name]]` (you can change sample)

    ## Methods
    - `create_placeholder(any_text)`      - format text like placeholder
    - `_format_args(args)`                - format args dict (kwargs) like placeholders
    - `format_template(template, kwargs)` - format temolate with placeholders
    '''
    _placeholder_format = "[[?{text if len > 0 else ' '}]]"

    def create_placeholder(self, any_text: str) -> str:
        scope = {'text':any_text, 'len':len(any_text)}
        return eval(f"f{repr(self._placeholder_format)}", globals=scope, locals=scope)

    def _format_args(self, args: dict[str, str]) -> dict[str, str]:
        # {'test':'data'} -> {create_placeholder('test'):'data'}
        result = {}
        for arg in args.keys():
            arg_formatted = self.create_placeholder(arg)
            result[arg_formatted] = args[arg]
        return result

    def format_template(self, template_text: str, **kwargs) -> str:
        '''
        ## format_template 
        Format template text with placeholders from kwargs.
        '''
        result = template_text
        args = self._format_args(kwargs)
        for templ in args.keys():
            result = result.replace(templ, args[templ])
        return result


def work_template(template: Template, **kwargs: str) -> str:
    '''
    # work_template
    Fromat your template with placeholders from kwargs.

    (defualts support)

    Use '__dict' arg for interprete value from that like kwargs.
    '''
    keyname = '__dict'
    if keyname in kwargs.keys():
        kwargs: dict[str, str] = kwargs[keyname]
        if not isinstance(kwargs, dict):
            raise SystemError(f"System kwargs key '{keyname}' must be type dict.")
    for key in kwargs:
        if not isinstance(kwargs[key], str):
            err = f'Invalid input type: kwargs keys must be type str \
(now: {type(kwargs[key])}). Warning skipped, type converted.'
            print(err)
            kwargs[key] = str(kwargs[key])
    te = TemplateEngine()
    template_text = template.template
    formatted = te.format_template(template_text, **kwargs)
    with_defaults = te.format_template(formatted, **template.defaults)
    return with_defaults



# === end file ===

if __TestAvailable:
    te = TemplateEngine()
    funcname = te.create_placeholder('funcname')
    templ = Template(f"""
def {funcname}():
    print("Hello, World!")
{funcname}()
    """, funcname="hello_world")
    print(templ.work(__dict={'funcname':"test"}))
    print(templ.template)