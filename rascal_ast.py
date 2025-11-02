from dataclasses import dataclass
from typing import Optional

class No:...

class Comando(No):...

class Expr(No):...

# --- Expressão ---

@dataclass
class Id(Expr):
    identificador: str

@dataclass
class Num(Expr):
    valor: int

class Bool(Expr):
    valor: bool

@dataclass
class ExprBin(Expr):
    op: str
    esq: Expr
    dir: Expr

@dataclass
class ExprUn(Expr):
    op: str
    expr: Expr

@dataclass
class ChamadaFuncao(Expr):
    nome: Id
    argumentos: list[Expr]

# --- Declaração ---

@dataclass
class Tipo(No):
    """
    Tipos possíveis: *integer* ou *boolean*.
    """
    nome: str

@dataclass
class Declaracao(No):
    """
    Declaração de variáveis ou parâmetros.
    """
    lista_ids: list[Id]
    tipo: Tipo

# --- Comando ---

@dataclass
class Atribuicao(Comando):
    id: Id
    expr: Expr

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
    variaveis: list[Id]

@dataclass
class Escrita(Comando):
    expressoes: list[Expr]

# --- Estrutura ---

@dataclass
class Bloco(No):
    pass

@dataclass
class Programa(No):
    nome: Id
    bloco: Bloco