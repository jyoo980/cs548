from typing import List

def methods_defined_on(obj) -> List[str]:
    callables = [
        method_name for method_name in dir(obj)
    ]
    return [name for name in callables if not _is_builtin(name)]

def _is_builtin(name) -> bool:
    return name.startswith("__") and name.endswith("__")
