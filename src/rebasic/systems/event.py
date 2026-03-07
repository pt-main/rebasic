# === start file ===
import asyncio
import inspect

class _EventSystem:
    def __init__(self, engine: 'Engine'):
        self._engine = engine
        self.handlers: dict[str, list[str]] = {'':[]}
        # handlers: 
        #    event: list[handlers]
        # handler: function(engine, event_system)
        self.event_history = []
        self._events = []
    
    def new_event(self) -> int:
        'generate numeric event and add this to events. returns event name'
        res = len(self._events)
        self._events.append(res)
        return res
    
    def add_handler(self, event: str, handler: object) -> None:
        if event in self.handlers:
            self.handlers[event] = [handler]
        else: self.handlers[event].append(handler)
    
    def add_event(self, event: str) -> None:
        self._events.append(event)
        self.handlers[event] = []
    
    def call_event(self, event: str) -> None:
        if event not in self._events:
            print(f'Warning: event is not found: {event}. Warning skipped.')
        handlers = self.handlers[event]
        for handler in handlers: 
            args = (self._engine, self)
            try:
                if inspect.iscoroutinefunction(handler): 
                    asyncio.run(handler(*args))
                else: handler(*args)
            except Exception as e:
                raise SystemError(f"Event '{event}' error in handler running: {e}")
        self.event_history.append(event)