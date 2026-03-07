from rebasic import Engine
# === start file ===


class _TextBackend:
    def __init__(self, trs: Engine):
        self._trs = engine
        engine.__backend__ = engine.context.constants.TEXT_GEN_FORMAT
        if engine.context._generation_format != engine.context.constants.TEXT_GEN_FORMAT:
            raise TypeError(
                f"Can't connect backend to trnaslator while generation format is not text."
            )
        engine.backend = self



class _NumericBackend:
    def __init__(self, engine: Engine):
        self._engine = engine
        engine.__backend__ = engine.context.constants.NUMERIC_GEN_FORMAT
        if engine.context._generation_format != engine.context.constants.NUMERIC_GEN_FORMAT:
            raise TypeError(
                f"Can't connect backend to trnaslator while generation format is not text."
            )
        engine.backend = self