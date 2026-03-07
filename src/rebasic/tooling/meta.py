from rebasic import Translator
# === start file ===

class MetaGeneration:
    def __init__(self, TranslatorSelf: Translator):
        self.__ts = TranslatorSelf

    def generate_cmd_docs(self) -> str:
        documentation = []
        commands = self.__ts.commands
        max_length = 0
        for cmd in commands.keys():
            if cmd in self.__ts._documentation_available:
                cmd_data = commands[cmd]
                max_length = max(len(cmd), max_length)
                documentation.append(f'|- {cmd}')
                for line in cmd_data['d'].split('\n'):
                    documentation.append(f'|    {line}')
        if len(documentation) > 0:
            max_length += 3
            sep = ('-' * max_length)
            final = f'''{sep}\n{'\n'.join(documentation)}\n{sep}'''
        else: final = 'has no documentation'
        return final
    
    def set_documentation_available_list(self, cmd_list: str):
        'add command to available docs list'
        self.__ts._documentation_available = cmd_list