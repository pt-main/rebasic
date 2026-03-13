# === start file ===

class Node:
    '''
    # Node
    Ast node for translator.
    '''
    class constants:
        NULL_NODE = 0
    type: str
    value: str
    def __init__(
        self, 
        type: str = None, 
        value: str = None, 
        meta: dict[str, any] = {}
    ):
        self.meta = meta
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Node(type={repr(self.type)}, value={repr(self.value)}, meta={self.meta})"
    
    def get(self, key: str, default: any = None):
        return self.meta.get(key, default)
    
    def __getitem__(self, __i: str):
        return self.get(__i, Node(type=self.constants.NULL_NODE, value=None))


def form_token_dict(
    raw: str, 
    tokens: list[Node], 
    switch: str | None = None
) -> dict[str, list[Node] | str]:
    if not isinstance(switch, str): switch = tokens[0].value.split('(')[0]
    return {'raw': raw, 'tokens': tokens, 'switch': switch}