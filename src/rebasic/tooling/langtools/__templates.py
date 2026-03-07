from rebasic.tooling import TemplateEngine
# === start file ===

class _Templates:
    __te = TemplateEngine()
    
    _python_func_template = f"""def {__te.create_placeholder('funcname')}\
({__te.create_placeholder('args')}) -> {__te.create_placeholder('returntype')}:
    {__te.create_placeholder('funcdocs')}
{__te.create_placeholder('funcbody')}"""

    _python_class_template = f"""class {__te.create_placeholder('classname')}\
({__te.create_placeholder('metaclasses')}):
    {__te.create_placeholder('classdocs')}
{__te.create_placeholder('classbody')}"""

    _clang_func_template = f"""{__te.create_placeholder('returntype')} \
{__te.create_placeholder('funcname')}({__te.create_placeholder('args')}) {{
{__te.create_placeholder('funcbody')}
}}"""