import re

_invalid = re.compile(r'[<>:"/\\|?*\x00-\x1F]')

def normalize_path_component(s: str, replacement: str = "_") -> str:
    # Replace invalid characters
    s = _invalid.sub(replacement, s.lower())

    # Remove path traversal
    s = re.sub(r"\.+", ".", s)       # collapse dots
    s = s.strip(" .")                # no leading/trailing dot or space

    # Collapse multiple replacements
    s = re.sub(rf"{re.escape(replacement)}+", replacement, s)

    return s or "unnamed"