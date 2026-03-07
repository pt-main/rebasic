# === start file ===
class RebasicError(Exception):
    '''
    # RebasicException
    Default rebasic exception.
    '''
    def __init__(
        self, 
        err: str, 
        line: str | None = None,
        index: int | None = None,
        action: str | None = None,
        naming: str = '',
    ) -> None:
        line = repr(line) if line is not None else '?'
        index = f'line {index}' if index is not None else 'line ?'
        context = f'{index} -=> {line}'
        text = f"{err}\n{context}" + (
            f"\n(On '{action}' action, {naming} language)" if action is not None else ''
        ) + '\n'
        super().__init__(text)

class RebasicRuntimeException(Exception):...
class RebasicSystemException(Exception):...
class RebasicException(Exception):...