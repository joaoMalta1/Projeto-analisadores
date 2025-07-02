# lex.py
# Nome: Joao Malta e Stella Maranhao

import ply.lex as lex

tokens = (
    'DISPOSITIVO',
    'DOIS_PONTOS',
    'ABRE_CHAVES',
    'FECHA_CHAVES',
    'VIRGULA',
    'SET',
    'IGUAL_SIMPLES',
    'NUM',
    'SE',
    'ENTAO',
    'SENAO',
    'LIGAR',
    'DESLIGAR',
    'ENVIAR',
    'ALERTA',
    'ABRE_PAREN',
    'FECHA_PAREN',
    'STRING',
    'PONTO',
    'MAIOR',
    'MENOR',
    'MAIORIGUAL',
    'MENORIGUAL',
    'IGUAL',
    'DIFERENTE',
    'ELOGICO',
    'PARA',
    'TODOS',
    'BOOL',
    'ID'
)

t_DOIS_PONTOS     = r':'
t_ABRE_CHAVES     = r'\{'
t_FECHA_CHAVES    = r'\}'
t_VIRGULA         = r','
t_IGUAL_SIMPLES   = r'='
t_ABRE_PAREN      = r'\('
t_FECHA_PAREN     = r'\)'
t_PONTO           = r'\.'
t_MAIOR           = r'>'
t_MENOR           = r'<'
t_MAIORIGUAL      = r'>='
t_MENORIGUAL      = r'<='
t_IGUAL           = r'=='
t_DIFERENTE       = r'!='
t_ELOGICO         = r'&&'

reserved = {
    'dispositivo': 'DISPOSITIVO',
    'set': 'SET',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'ligar': 'LIGAR',
    'desligar': 'DESLIGAR',
    'enviar': 'ENVIAR',
    'alerta': 'ALERTA',
    'para': 'PARA',
    'todos': 'TODOS',
    'TRUE': 'BOOL',
    'FALSE': 'BOOL'
}

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value.strip('"')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t\n\r'

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
