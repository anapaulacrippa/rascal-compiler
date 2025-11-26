import sys
import ply.yacc as yacc
from lexer import tokens, make_lexer
import rascal_ast as ast
from rascal_semantico import TIPO_INT, TIPO_BOOL

precedence = (
    ("nonassoc", "IFS"),
    ("nonassoc", "ELSE"),
    ("right", "NOT"),
    ("nonassoc", "=", "DIF", "<", "LE", ">", "GE"),
    ("left", '+', '-', 'OR'),
	("left", '*', 'DIV', 'AND'),
    ("right", 'NEG')
)

# --- Regras do Programa e Bloco ---

def p_programa(p):
    """programa : PROGRAM ID ';' bloco PT"""
    p[0] = ast.Programa(nome=ast.Id(p[2]), bloco=p[4])

def p_bloco(p):
    """bloco : secao_vars secao_subrots cmd_composto"""
    p[0] = ast.Bloco(secao_variaveis=p[1], secao_subrotinas=p[2], cmd_composto=p[3])


# --- Seção de Variáveis ---

def p_secao_vars(p):
    """secao_vars : VAR lista_decl_vars"""
    p[0] = p[2]

def p_secao_vars_vazia(p):
    """secao_vars : """
    p[0] = []

def p_lista_decl_vars(p):
    """lista_decl_vars : decl_var ';' lista_decl_vars
                       | decl_var ';'"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_decl_vars(p):
    """decl_var : lista_ids ':' tipo"""
    p[0] = ast.DeclaracaoVar(lista_ids=p[1], tipo=p[3])

def p_lista_ids(p):
    """lista_ids : ID ',' lista_ids
                 | ID"""
    if len(p) == 4:
        p[0] = [ast.Id(p[1])] + p[3]
    else:
        p[0] = [ast.Id(p[1])]

def p_tipo(p):
    """tipo : BOOL
            | INT"""
    if p[1] == 'inteiro':
        p[0] = TIPO_INT
    else:
        p[0] = TIPO_BOOL

'''def p_opcional_ids(p):
    """opcional_ids : ',' ID opcional_ids"""
    p[0] = ast.Id(p[2]) + p[3]
def p_opcional_ids_vazio(p):
    """opcional_ids : """
    p[0] = []'''

# --- Seção de Subrotinas ---

def p_secao_subrots(p):
    """secao_subrots : decl_proc ';' secao_subrots
                     | decl_func ';' secao_subrots
                     | """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

def p_sec_declarar_subrots_vazio(p):
    """sec_declarar_subrots : """
    pass

def p_decl_proc(p):
    """decl_proc : PROCEDURE ID param_formais ';' bloco"""
    p[0] = ast.DeclaracaoProc(id=ast.Id(p[2]), params=p[3], bloco=p[5])

def p_declarar_func(p):
    """declarar_func : FUNCTION ID param_formais ':' tipo ';' bloco_subrot"""
    p[0] = ast.DeclaracaoFunc(id=ast.Id(p[2]), param_formais=(ast.ParamFormais(p[3])), tipo=ast.Tipo(p[5]), bloco_subrot=(ast.BlocoSubrot(p[7])))

def p_bloco_subrot(p):
    """bloco_subrot : sec_declarar_vars cmd_composto"""
    p[0] = ast.BlocoSubrot(comando=p[2])

def p_param_formais(p):
    """param_formais : '(' dec_params opcional_dec_params ')'"""
    p[0] = ast.ParamFormais(p[2])
def p_param_formais_vazio(p):
    """param_formais : """
    p[0] = []

def p_opcional_dec_params(p):
    """opcional_dec_params : ';' dec_params opcional_dec_params"""
    p[0] = ast.DecParams(p[2]) + p[3]
def p_opcional_dec_params_vazio(p):
    """opcional_dec_params : """
    p[0] = []

def p_dec_params(p):
    """dec_params : lista_ids ':' tipo"""
    p[0] = ast.DecParams(lista_ids=p[1], tipo=p[3])

def p_cmd_composto(p):
    """cmd_composto : BEGIN cmd opcional_cmd END"""
    p[0] = p[3].append(p[2])

def p_opcional_cmd(p):
    """opcional_cmd : ';' cmd opcional_cmd"""
    p[0] = p[3].append(p[2])
def p_opcional_cmd_vazio(p):
    """opcional_cmd : """
    p[0] = ast.ComandoComposto(lista_cmds=[])

def p_cmd(p):
    """cmd : atribuicao
            | chamada_proc
            | condicional
            | repeticao
            | leitura
            | escrita
            | cmd_composto"""
    p[0] = p[1]

def p_atribuicao(p):
    """atribuicao : ID ATTRIB expr"""
    p[0] = ast.Atribuicao(id=ast.Id(p[1]), expr=p[3])

def p_chamada_proc(p):
    """chamada_proc : ID '(' lista_expr ')'"""
    p[0] = ast.ChamadaProc(nome=ast.Id(p[1]), argumentos=p[3])

def p_condicional_simples(p):
    """condicional : IF expr THEN cmd %prec IFS"""
    p[0] = ast.Condicional(condicao=p[2], comando_then=p[4])

def p_condicional_else(p):
    """condicional : IF expr THEN cmd ELSE cmd"""
    p[0] = ast.Condicional(condicao=p[2], comando_then=p[4], comando_else=p[6])

def p_repeticao(p):
    """repeticao : WHILE expr DO cmd"""
    p[0] = ast.Repeticao(condicao=p[2], comando=p[4])

def p_leitura(p):
    """leitura : READ '(' lista_ids ')'"""
    p[0] = ast.Leitura(variavais=p[3])

def p_escrita(p):
    """escrita : WRITE '(' lista_expr ')'"""
    p[0] = ast.Escrita(expressoes=p[3])

def p_lista_expr(p):
    """lista_expr : expr opcional_expr"""
    p[0] = ast.Expr(p[1]) + p[2]
def p_lista_expr_vazio(p):
    """lista_expr : """
    p[0] = []

def p_opcional_expr(p):
    """opcional_expr : ',' expr opcional_expr"""
    pass
def p_opcional_expr_vazio(p):
    """opcional_expr : """
    pass

def p_expr(p):
    """expr : expr_simples opcional_relacao"""
    p[0] = ast.Expr(p[1]) + p[2]

def p_opcional_relacao(p):
    """opcional_relacao : relacao expr_simples"""
    p[0] = p[1] + ast.Expr(p[2])
def p_opcional_relacao_vazio(p):
    """opcional_relacao : """
    p[0] = []

def p_relacao(p):
    """relacao : '='
                | DIF
                | '<'
                | LT
                | '>'
                | GE"""
    p[0] = p[1]

def p_expr_simples(p):
    """expr_simples : termo opcional_termo"""
    p[0] = p[2].append(ast.Termo(p[1]))

def p_opcional_termo(p):
    """opcional_termo : '+' termo opcional_termo
                        | '-' termo opcional_termo
                        | OR termo opcional_termo"""
    p[0] = p[3].append(ast.Termo(p[2]))
def p_opcional_termo_vazio(p):
    """opcional_termo : """
    p[0]= ast.ExprSimples(termos=[])

def p_termo(p):
    """termo : fator opcional_fator"""
    p[0] = p[2].append(ast.Fator(p[1]))

def p_opcional_fator(p):
    """opcional_fator : '*' fator opcional_fator
                        | DIV fator opcional_fator
                        | AND fator opcional_fator"""
    p[0] = p[3].append(ast.Fator(valor=p[2]))
def p_opcional_fator_vazio(p):
    """opcional_fator : """
    p[0] = ast.Termo(fatores=[])

def p_fator(p):
    """fator : variavel
            | NUM
            | logico
            | chamada_funcao
            | '(' expr ')'
            | NOT fator
            | NEG fator"""
    if p[1] == '(' or p[1] == 'NOT' or p[1] == 'NEG':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_variavel(p):
    """variavel : ID"""
    p[0] = ast.Id(p[1])

def p_logico(p):
    """logico : TRUE
              | FALSE"""
    p[0] = p[1]

def p_chamada_fucao(p):
    """chamada_funcao : ID '(' lista_expr ')'"""
    p[0] = ast.ChamadaFuncao(nome=ast.Id(p[1]), argumentos=p[3])

# Erro sintático
def p_error(tok):
    if tok is None:
        print("ERRO SINTÁTICO: fim de arquivo inesperado (EOF).")
    else:
        print(f"ERRO SINTÁTICO na linha {tok.lineno}: token inesperado ({tok.value!r})")

# Instancia o parser
def make_parser():
    return yacc.yacc(start="programa")

# Para testar o parser: python3 parser.py < exemplo.ras
if __name__ == "__main__":
    data = sys.stdin.read()
    parser = make_parser()
    parser.parse(data, lexer=make_lexer())
