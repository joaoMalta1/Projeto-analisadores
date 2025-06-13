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
    'TRUE': 'TRUE',
    'FALSE': 'FALSE',
}

tokens += list(reserved.values())

# Expressões regulares para os símbolos
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

# Regras para tokens específicos
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'TRUE|FALSE'
    t.type = reserved.get(t.value, 'BOOL')
    t.value = True if t.value == 'TRUE' else False
    return t

def t_NAMEDEVICE(t):
    r'[A-Za-z_][A-Za-z0-9_]*' #comeca com letra e dps pode ter letra e numero 
    t.type = reserved.get(t.value, 'NAMEDEVICE')  # se for palavra reservada, substitui
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Inicializa o analisador léxico
lexer = lex.lex()
