#Nome: Joao Malta e Stella Maranhao

import ply.lex as lex

# Lista de tokens
tokens = [
    'NUM',
    'BOOL',
    'STRING',
    'NAMEDEVICE',
    'OBSERVATION',

    'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL', 'IGUAL', 'DIFERENTE',
    'ELOGICO',

    'DOIS_PONTOS',
    'ABRE_CHAVES', 'FECHA_CHAVES',
    'ABRE_PAREN', 'FECHA_PAREN',
    'VIRGULA', 'PONTO',
]

# Palavras reservadas
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
    'FALSE': 'BOOL',
}

tokens += list(reserved.values())

# Regex
t_MAIOR       = r'>'
t_MENOR       = r'<'
t_MAIORIGUAL  = r'>='
t_MENORIGUAL  = r'<='
t_IGUAL       = r'=='
t_DIFERENTE   = r'!='
t_ELOGICO     = r'&&'

t_DOIS_PONTOS = r':'
t_ABRE_CHAVES = r'\{'
t_FECHA_CHAVES = r'\}'
t_ABRE_PAREN  = r'\('
t_FECHA_PAREN = r'\)'
t_VIRGULA     = r','
t_PONTO       = r'\.'

t_ignore = ' \t'

# Regras
def t_STRING(t):
    r'"[^"]+"' 
    t.value = t.value[1:-1] #tira aspas
    return t

def t_NUM(t): #só pode aceitar positivo
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'TRUE|FALSE'
    t.type = reserved.get(t.value, 'BOOL')
    t.value = (t.value == 'TRUE' )
    return t

def t_NAMEDEVICE(t):
    r'[A-Za-z]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = 'NAMEDEVICE'
    return t

def t_OBSERVATION(t):
    r'[A-Za-z][A-Za-z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = 'OBSERVATION'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Inicializa o analisador léxico
lexer = lex.lex()