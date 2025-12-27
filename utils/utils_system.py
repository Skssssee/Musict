# utils/utils_system.py

from pytgcalls import PyTgCalls
from utils.logger import LOGGER

_call = None

def get_call():
    global _call
    if _call is None:
        from assistants.assistant_system import assistant
        _call = PyTgCalls(assistant)
    return _call
