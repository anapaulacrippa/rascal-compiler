import sys
import ply.lex as lex

# Palavras reservadas
reserved = {
    'program': 'PROGRAM',
    'procedure': 'PROCEDURE',
    'function': 'FUNCTION',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    'integer': 'INT',
    'boolean': 'BOOL',
    'false': 'FALSE',
    'true': 'TRUE',
    'while': 'WHILE',
    'do': 'DO',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'read': 'READ',
    'write': 'WRITE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'div': 'DIV',
}

# Tokens nomeados
tokens = (
    'ID',
    'NUM',
    'PT',     # .
    'ATTRIB', # :=
    'DIF',    # <>
    'GE',     # >=
    'LE',     # <=
) + tuple(reserved.values())

# Tokens literais
literals = ['=', '+', '-', '*', '(', ')', ':', ';', ',', '>', '<']
# Regras simples
t_PT = r'\.'
t_DIF = r'<>'
t_ATTRIB = r':='
t_GE = r'>='  # greater equal
t_LE = r'<='  # less equal

# Números Inteiros
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificadores válidos + palavras reservadas
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Espaços e tabulações
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

""" # Comentários de linha (// até o fim da linha)
def t_COMMENT(t):
    r'//[^\n]*'
    pass """

# Erros léxicos
def t_error(t):
    print(f"ERRO LÉXICO na linha {t.lineno}: símbolo ilegal {t.value[0]!r}")
    t.lexer.skip(1)

# Instancia o lexer
def make_lexer():
    return lex.lex()
    

# Para testar o lexer sozinho: python3 lexer.py < exemplo.rascal
if __name__ == '__main__':
    data = sys.stdin.read()
    lexer = make_lexer()
    lexer.input(data)
    for tok in lexer:
        print(f'<{tok.type}, {tok.value!r}> na linha: {tok.lineno}')
