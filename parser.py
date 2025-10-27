# parser.py
import sys
import ply.yacc as yacc
from lexer import tokens, make_lexer
from ast_calculadin import *

precedence = (
    ("nonassoc", "IF", "THEN", "ELSE"),
    ("right", "NOT"),
    ("nonassoc", "=", "DIF", "<", "LT", ">", "GT"),
    ("left", '+', '-'),
	("left", '*', 'DIV'),
    ("right", 'UMENOS')
)

# Regras gramaticais
def p_programa(p):
    """programa : PROGRAM ID ';' bloco PT"""
    pass

def p_bloco(p):
    """bloco: sec_declarar_vars sec_declarar_subrots cmd_composto"""
    pass

def p_sec_declarar_vars(p):
    """sec_declarar_vars : VAR declarar_vars ';' opcional_dec_vars"""
    pass
def p_sec_declarar_vars_vazia(p):
    """sec_declarar_vars : """
    pass

def p_opcional_dec_vars(p):
    """opcional_dec_vars : declarar_vars ';'"""
    pass
def p_opcional_dec_vars_vazia(p):
    """opcional_dec_vars : """
    pass

def p_declarar_vars(p):
    """declarar_vars : lista_ids ':' tipo"""

def p_lista_ids(p):
    """lista_ids : ID opcional_ids"""
    pass

def p_opcional_ids(p):
    """opcional_ids : ',' ID"""
    pass
def p_opcional_ids_vazia(p):
    """opcional_ids : """
    pass

def p_tipo(p):
    """tipo : BOOL | INT"""
    pass

def p_sec_declarar_subrots(p):
    """sec_declarar_subrots : declarar_proc ';'
                            | declarar_func ';'"""
    pass
def p_sec_declarar_subrots_vazia(p):
    """sec_declarar_subrots : """
    pass

def p_declarar_proc(p):
    """declarar_proc : PROCEDURE ID param_formais ';' bloco_subrot"""
    pass

def p_declarar_func(p):
    """declarar_func : FUNCTION ID param_formais ':' tipo ';' bloco_subrot"""
    pass

def p_bloco_subrot(p):
    """bloco_subrot : sec_declarar_vars cmd_composto"""
    pass

def p_param_formais(p):
    """param_formais : '(' dec_params opcional_dec_params ')'"""
    pass
def p_param_formais_vazia(p):
    """param_formais : """
    pass

def p_opcional_dec_params(p):
    """opcional_dec_params : ';' dec_params"""
    pass
def p_opcional_dec_params_vazia(p):
    """opcional_dec_params : """
    pass

def p_dec_params(p):
    """dec_params : lista_ids ':' tipo"""
    pass

def p_cmd_composto(p):
    """cmd_composto : BEGIN cmd opcional_cmd END"""
    pass

def p_opcional_cmd(p):
    """opcional_cmd : ';' cmd"""
    pass
def p_opcional_cmd_vazia(p):
    """opcional_cmd : """
    pass

def p_cmd(p):
    """cmd : atribuicao | chamada_proc | condicional | repeticao | leitura | escrita | cmd_composto"""
    pass

def p_atribuicao(p):
    """atribuicao : ID ATTRIB expr"""
    pass

def p_chamada_proc(p):
    """chamada_proc : ID '(' lista_expr ')'"""
    pass

def p_condicional(p):
    """condicional : IF expr THEN cmd opcional_else"""
    pass

def p_opcional_else(p):
    """opcional_else : ELSE cmd"""
    pass
def p_opcional_else_vazia(p):
    """opcional_else : """
    pass

def p_repeticao(p):
    """repeticao : WHILE expr DO cmd"""
    pass

def p_leitura(p):
    """leitura : READ '(' lista_ids ')'"""
    pass

def p_escrita(p):
    """escrita : WRITE '(' lista_expr ')'"""
    pass

def p_lista_expr(p):
    """lista_expr : expr opcional_expr"""
    pass
def p_lista_expr_vazia(p):
    """list_expr : """
    pass

def p_opcional_expr(p):
    """opcional_expr : ',' expr"""
    pass
def p_opcional_expr_vazia(p):
    """opcional_expr : """
    pass

def p_expr(p):
    """expr : expr_simples opcional_relacao"""
    pass

def p_opcional_relacao(p):
    """opcional_relacao : relacao expr_simples"""
    pass
def p_opcional_relacao_vazia(p):
    """opcional_relacao : """
    pass

def p_relacao(p):
    """relacao : '=' | '<>' | '<' | '<=' | '>' | '>='"""
    pass

def p_expr_simples(p):
    """expr_simples : termo opcional_termo"""
    pass

def p_opcional_termo(p):
    """opcional_termo : '+' termo | '-' termo | OR termo"""
    pass
def p_opcional_termo_vazia(p):
    """opcional_termo : """
    pass

def p_termo(p):
    """termo : fator opcional_fator"""
    pass

def opcional_termo(p):
    """opcional_termo : '*' fator | DIV fator | AND fator"""
    pass
def opcional_termo_vazia(p):
    """opcional_termo : """
    pass

# Erro sintático
def p_error(tok):
    if tok is None:
        print("ERRO SINTÁTICO: fim de arquivo inesperado (EOF).")
    else:
        print(f"ERRO SINTÁTICO na linha {tok.lineno}: token inesperado ({tok.value!r})")

# Instancia o parser
def make_parser():
    return yacc.yacc(start="programa")

# Para testar o parser: python3 parser.py <exemplo.calc
if __name__ == "__main__":
    data = sys.stdin.read()
    parser = make_parser()
    parser.parse(data, lexer=make_lexer())
    print()
