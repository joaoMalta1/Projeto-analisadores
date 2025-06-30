# lex.py
# Nome: Joao Malta e Stella Maranhao

import ply.lex as lex

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

# Lista de tokens. Inclui todos os tokens que não são palavras reservadas
# mas que o lexer precisa identificar. As palavras reservadas serão adicionadas
# via `reserved.values()`.
tokens = [
    'NUM',
    'STRING',
    'NAMEDEVICE',
    'OBSERVATION',

    'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL', 'IGUAL', 'DIFERENTE',
    'ELOGICO',

    'DOIS_PONTOS',
    'ABRE_CHAVES', 'FECHA_CHAVES',
    'ABRE_PAREN', 'FECHA_PAREN',
    'VIRGULA', 'PONTO',
    'IGUAL_SIMPLES'
]

# Adiciona todos os valores do dicionário 'reserved' à lista 'tokens'
# Isso garante que as palavras reservadas sejam reconhecidas como seus respectivos tokens.
tokens += list(reserved.values())

# Regex para tokens simples
t_MAIOR        = r'>'
t_MENOR        = r'<'
t_MAIORIGUAL   = r'>='
t_MENORIGUAL   = r'<='
t_IGUAL        = r'=='
t_DIFERENTE    = r'!='
t_ELOGICO      = r'&&'
t_IGUAL_SIMPLES = r'='

t_DOIS_PONTOS  = r':'
t_ABRE_CHAVES  = r'\{'
t_FECHA_CHAVES = r'\}'
t_ABRE_PAREN   = r'\('
t_FECHA_PAREN  = r'\)'
t_VIRGULA      = r','
t_PONTO        = r'\.'

t_ignore = ' \t'

# Regras para tokens mais complexos
def t_STRING(t):
    r'"[^"]+"'
    t.value = t.value[1:-1] # Remove as aspas
    return t

def t_NUM(t): # Só pode aceitar positivo
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'TRUE|FALSE'
    # Aqui, a palavra reservada já garante que o tipo será 'BOOL'.
    # Apenas convertemos o valor para booleano Python.
    t.value = (t.value == 'TRUE')
    return t

def t_OBSERVATION(t):
    r'[A-Za-z][A-Za-z0-9]*'
    # Verifica se a string é uma palavra reservada.
    # Se for, usa o tipo da palavra reservada.
    # Caso contrário, é uma 'OBSERVATION'.
    t.type = reserved.get(t.value, 'OBSERVATION')
    return t

def t_NAMEDEVICE(t):
    r'[A-Za-z]+'
    # Verifica se a string é uma palavra reservada.
    # Se for, usa o tipo da palavra reservada (ex: 'SET', 'LIGAR').
    # Caso contrário, é um 'NAMEDEVICE'.
    t.type = reserved.get(t.value, 'NAMEDEVICE')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Inicializa o analisador léxico
lexer = lex.lex()