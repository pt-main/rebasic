# === start file ===

class _LangGenerator:
    '''
    # _LangGenerator
    Generation tools for rebasic.
    '''
    def __init__(self):
        self.reset()

    def reset(self):
        self.__name_counter: int = 0
    
    @property
    def _unique_name(self) -> str:
        self.__name_counter += 1
        return f"__unique{self.__name_counter}"