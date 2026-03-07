from rebasic import Translator
# === start file ===


class _TextBackend:
    def __init__(self, trs: Translator):
        self._trs = trs
        trs.__backend__ = trs.context.constants.TEXT_GEN_FORMAT
        if trs.context._generation_format != trs.context.constants.TEXT_GEN_FORMAT:
            raise TypeError(
                f"Can't connect backend to trnaslator while generation format is not text."
            )
        trs.backend = self



class _NumericBackend:
    def __init__(self, trs: Translator):
        self._trs = trs
        trs.__backend__ = trs.context.constants.NUMERIC_GEN_FORMAT
        if trs.context._generation_format != trs.context.constants.NUMERIC_GEN_FORMAT:
            raise TypeError(
                f"Can't connect backend to trnaslator while generation format is not text."
            )
        trs.backend = self