from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int] = None
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
