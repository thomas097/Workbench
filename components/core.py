from typing import Literal
from dataclasses import dataclass

@dataclass
class Badge:
    label: str
    icon: str
    color: Literal['red', 'orange', 'yellow', 'blue', 'green', 'violet', 'gray', 'primary']