from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: Optional[int] = None
    nome: Optional[str] = None
    desc: Optional[str] = None
    valor: Optional[float] = None
    quant: Optional[int] = None
    fornecedor: Optional[str] = None
