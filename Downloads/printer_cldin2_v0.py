from __future__ import annotations
import ast_cldin2 as ast
from defs_cldin2 import Visitador
import sys

class ImpressoraAST(Visitador):
    def __init__(self, saida=sys.stdout):
        self.saida = saida

    def imprime(self, texto: str):
        self.saida.write(texto)
    
    def visita_Programa(self, no: ast.Programa):
        self.imprime("(Programa")
        self.visita(no.bloco_cmds)
        self.imprime(")")

    def visita_BlocoCmds(self, no: ast.BlocoCmds):
        self.imprime("(Comandos")
        for c in no.lista_cmds:
            self.imprime(" ")
            self.visita(c)
        self.imprime(")")
    
    def visita_Declaracao(self, no: ast.Declaracao):
        self.visita(no.id)
        self.imprime(": " + no.nome_tipo)
    
    def visita_Condicional(self, no: ast.Condicional):
        self.imprime("if ")
        self.visita(no.condicao)
        self.visita(no.bloco_then)
        if no.bloco_else:
            self.imprime("else")
            self.visita(no.bloco_else)
    
    def visita_Funcao(self, no: ast.Funcao):
        self.imprime(f"({no.nome_funcao}")
        self.visita(no.argumento)
        self.imprime(")")

    def visita_Atribuicao(self, no: ast.Atribuicao):
        self.visita(no.id)
        self.imprime("=")
        self.visita(no.calculo)
    
    def visita_CalculoBinario(self, no: ast.CalculoBinario):
        self.visita(no.esq)
        self.imprime(no.op)
        self.visita(no.dir)
    
    def visita_CalculoUnario(self, no: ast.CalculoUnario):
        self.imprime(no.op)
        self.visita(no.calculo)
    
    def visita_CmdId(self, no: ast.CmdId):
        self.imprime(no.nome)
    
    def visita_CmdConstNum(self, no: ast.CmdConstNum):
        self.imprime(f"{no.valor}")
    
    def visita_CmdConstBool(self, no: ast.CmdConstBool):
        self.imprime(f"{no.valor}")
