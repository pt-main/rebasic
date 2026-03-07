from base import Node, form_token_dict

# === start file ===

class ParserMeta:
    '''
    # ParserMeta
    Metaclass for any parsers in rebasic.
    '''
    tokens: list[dict[str, list[Node] | str]]

    def __init__(self): self.reset()

    def reset(self): raise NotImplementedError
    
    def parse(self, string: str) -> list[dict[str, list[Node] | str]]:
        raise NotImplementedError

    def eat(self, raw_line: str, tokens: list[Node]):
        to_append = form_token_dict(raw=raw_line, tokens=tokens)
        self.tokens.append(to_append)
    
    def form(self, line: str) -> list[Node]:
        raise NotImplementedError
    
    def __call__(self, string: str) -> list[dict[str, list[Node] | str]]:
        self.reset()
        return self.parse(string=string)