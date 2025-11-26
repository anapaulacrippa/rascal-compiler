from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from rascal_defs import Simbolo, Tipo

class No:...

class Comando(No):...

class Expr(No):...
    # tipo: Tipo | None = None

# --- Estrutura geral do programa ---

@dataclass
class Programa(No):
    nome: Id
    bloco: Bloco
    total_vars: int = 0
    
@dataclass
class Bloco(No):
    """
    Pode conter declarações ou comandos.
    """
    secao_variaveis: List[DeclaracaoVar] = field(default_factory=list)
    secao_subrotinas: List[DeclaracaoProc | DeclaracaoFunc] = field(default_factory=list)
    cmd_composto: CmdComposto | None = None

# --- Declarações ---

@dataclass
class DeclaracaoVar(No):
    lista_ids: List[Id]
    tipo: Tipo # ou tipo: str?

@dataclass
class DeclaracaoProc(No):
    id: Id
    params: List[ParamsFormais]
    bloco: Bloco

@dataclass
class DeclaracaoFunc(No):
    id: Id
    params: List[ParamsFormais]
    tipo_retorno: Tipo
    bloco: Bloco

@dataclass
class ParamsFormais(No):
    lista_ids: List[Id]
    tipo: Tipo
    # passagem por valor ou por referencia
    por_referencia: bool = False

# --- Expressões ---

@dataclass
class Id(Expr):
    nome: str
    simbolo: Simbolo | None = None

@dataclass
class Num(Expr):
    valor: int

class Bool(Expr):
    valor: bool

@dataclass
class ExprBin(Expr):
    """
    +, -, *, div, and, or, =, <>, <, <=, >, >=
    """
    op: str
    esq: Expr
    dir: Expr

@dataclass
class ExprUn(Expr):
    """
    -, not
    """
    op: str
    expr: Expr

@dataclass
class ChamadaFunc(Expr):
    nome: Id
    argumentos: List[Expr]

# --- Comandos ---

@dataclass
class Atribuicao(Comando):
    id: Id
    expr: Expr

@dataclass
class ChamadaProc(Comando):
    nome: Id
    argumentos: List[Expr]

@dataclass
class Condicional(Comando):
    condicao: Expr
    comando_then: Comando
    comando_else: Optional[Comando] = None

@dataclass
class Repeticao(Comando):
    condicao: Expr
    comando: Comando

@dataclass
class Leitura(Comando):
    variaveis: List[Id]

@dataclass
class Escrita(Comando):
    expressoes: List[Expr]

@dataclass
class CmdComposto(Comando):
    lista_cmds: List[Comando]