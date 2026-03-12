from pathlib import Path
_CACHE: dict[str, str] = {}
def load_prompt(name: str) -> str:
    if name not in _CACHE:
        path = Path(__file__).parent / f"{name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        _CACHE[name] = path.read_text(encoding="utf-8")
    return _CACHE[name]
