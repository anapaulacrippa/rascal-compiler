from __future__ import annotations
from typing import List, Dict
#from rascal_gerador_mepa import Visitador
from dataclasses import dataclass, field
import rascal_ast as ast

class Tipo:...

@dataclass(frozen=True)
class TipoInt(Tipo):
    def __str__(self) -> str: return "inteiro"

@dataclass(frozen=True)
class TipoBool(Tipo):
    def __str__(self) -> str: return "booleano"

TIPO_INT = TipoInt()
TIPO_BOOL = TipoBool()

class Categoria:
    VAR = 'var'
    PARAM = 'param'
    PROG = 'program'

@dataclass
class Simbolo:
    nome: str
    categoria: str
    tipo: Tipo | None = None

    # campos para geração de código
    escopo: int = 0
    deslocamento: int = 0

    # campos PROG/PROC/FUNC
    total_locais: int = 0   # qtde para AMEM/DMEM
    total_params: int = 0   # qtde para RTPR

    # campos para análise semântica
    params_info: List[Tipo] = field(default_factory=list)
    simbolo_retorno: Simbolo | None = None
    retornos_encontrados: int = 0


class TabelaSimbolos:
    def __init__(self):
        # nome do identificador ; informações do identificador
        self.escopos: List[Dict[str, Simbolo]] = [dict()] # escopo 0 = global
        self.deslocamento_atual: int = 0

    def abre_escopo(self):
        self.escopos.append({})

    def fecha_escopo(self):
        if len(self.escopos) > 1:
            self.escopos.pop()

    @property
    def nivel(self) -> int:
        return len(self.escopos) - 1

    def instala(self, s: Simbolo) -> str | None:
        atual = self.escopos[-1]
        if s.nome in atual:
            return f"Identificador '{s.nome}' já declarado neste escopo."
        s.escopo = self.nivel
        atual[s.nome] = s
        return None
    
    def busca(self, nome: str) -> Simbolo | None:
        for tabela in reversed(self.escopos):
            if nome in tabela:
                return tabela[nome]
        return None