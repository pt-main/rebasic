# === start file ===
import time

class _LangState:
    '''
    # LangState
    State of translator.
    '''
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.DEBUG_MODE: bool = False
        self.LOGGING_MODE: bool = True
        self._logs: list[str] = []
        self._max_status_len = 0
    
    def _add_log(self, log: str, status: str = 'info') -> None:
        to_add = f"{
            str(time.time()).center(18, ' ')
        } [{
            status.center(self._max_status_len, ' ')
        }] [{log}]"
        self._logs.append(to_add)
        return to_add
    
    def _log(self, log: str, status: str = 'info'):
        self._max_status_len = max(len(status), self._max_status_len)
        log_text = self._add_log(
            log=log, 
            status=status,
        )
        if self.DEBUG_MODE: print(log_text)