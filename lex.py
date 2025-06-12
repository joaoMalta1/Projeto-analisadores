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



# Inicializa o analisador léxico
lexer = lex.lex()
