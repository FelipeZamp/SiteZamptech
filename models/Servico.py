from dataclasses import dataclass
from typing import Optional

@dataclass
class Servico:
    id: Optional[int] = None
    nome: Optional[str] = None
    desc: Optional[str] = None
    valor: Optional[float] = None
