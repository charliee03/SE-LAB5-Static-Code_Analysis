| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument (`logs=[]`) | Bug | ~12 | Mutable default list shared across function calls can retain state between calls | Changed default to `None` and initialize a new list inside `add_item` |
| Broad `except:` (overly general) | Logic / Maintainability | ~30 | Catches all exceptions and hides real errors | Replaced with specific `KeyError` and `TypeError` handling in `remove_item` |
| Missing module/function docstrings | Style | multiple | Pylint flagged missing docstrings which reduce readability and tooling usefulness | Added a module docstring and a docstring for `main` and `add_item` functions |
| Logging uses f-strings in logging calls | Performance / Style | multiple | Logging f-strings cause interpolation even when message is filtered | Replaced f-strings with lazy logging formatting (e.g., `logger.info("msg %s", val)`) |
| Rebinding global `stock_data` in load_data | Logic | ~40 | Reassigning the module-level dict requires `global` and can break references | Update in-place by `stock_data.clear()` and `stock_data.update(data)` so callers keep references |
| Long line (PEP8) | Style | 12 | Line exceeded 79 chars (Flake8 E501) | Wrapped `logging.basicConfig(...)` parameters across multiple lines to satisfy line length |
