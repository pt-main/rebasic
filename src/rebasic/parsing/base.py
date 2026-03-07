# === start file ===
class Node:
    '''
    # Node
    Ast node for translator.
    '''
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
        return f"Node(type={repr(self.type)}, value={repr(self.value)})"


def form_token_dict(raw: str, tokens: list[Node]) -> dict[str, list[Node] | str]:
    return {'raw': raw, 'tokens': tokens}