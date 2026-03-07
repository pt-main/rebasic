# === start file ===

class _CodeState:
    '''
    # CodeState
    State of code.
    '''
    macroses: dict[str, list[str]] = {}
    code_blocks: dict[str, list[str]] = {}