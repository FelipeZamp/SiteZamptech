from dataclasses import dataclass
from typing import Optional

@dataclass
class Ordem:
    id: Optional[int] = None
    cliente: Optional[str] = None
    servico: Optional[str] = None
    status: Optional[str] = None
    desc: Optional[str] = None
