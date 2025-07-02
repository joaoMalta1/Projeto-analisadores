import ply.yacc as yacc
from lex import tokens

codigo_gerado = []
variaveis = {}          
dispositivos = set()
declaracoes = []

def flatten(lst):
    flat = []
    for item in lst:
        if isinstance(item, list):
            flat.extend(flatten(item))
        elif item is not None and item != '':
            flat.append(item)
    return flat

# --- CABEÇALHO DO C ---
cabecalho_c = [
    '#include <stdio.h>',
    '#include <string.h>',
    '',
    'void ligar(char* d) { printf("%s ligado!\\n", d); }',
    'void desligar(char* d) { printf("%s desligado!\\n", d); }',
    'void alerta(char* d, char* msg) {',
    '    printf("%s recebeu o alerta:\\n", d);',
    '    printf("%s\\n", msg);',
    '}',
    'void alerta_com_valor(char* d, char* msg, int val) {',
    '    printf("%s recebeu o alerta:\\n", d);',
    '    printf("%s %d\\n", msg, val);',
    '}',
    '',
    'int main() {'
]

fim_c = [
    '    return 0;',
    '}'
]

# --- GRAMÁTICA ---

def p_program(p):
    '''program : devices cmds'''
    global codigo_gerado
    codigo_gerado = cabecalho_c + flatten(declaracoes) + flatten(p[2]) + fim_c
    p[0] = codigo_gerado


def p_devices_multiple(p):
    '''devices : device devices'''
    p[0] = [p[1]] + p[2]

def p_devices_single(p):
    '''devices : device'''
    p[0] = [p[1]]

def p_device_obs(p):
    '''device : DISPOSITIVO DOIS_PONTOS ABRE_CHAVES ID VIRGULA ID FECHA_CHAVES'''
    dispositivo = p[4]
    observacao = p[6]
    dispositivos.add(dispositivo)
    dispositivos.add(observacao)
    declaracoes.append(f'    int {dispositivo} = 0;')
    declaracoes.append(f'    int {observacao} = 0;')
    variaveis[observacao] = 'int'
    p[0] = f'    /* dispositivo {dispositivo} e observação {observacao} declarados */'


def p_device_simple(p):
    '''device : DISPOSITIVO DOIS_PONTOS ABRE_CHAVES ID FECHA_CHAVES'''
    dispositivo = p[4]
    dispositivos.add(dispositivo)
    declaracoes.append(f'    int {dispositivo} = 0;')
    p[0] = f'    /* dispositivo {dispositivo} declarado */'


def p_cmds_multiple(p):
    '''cmds : cmd PONTO cmds'''
    p[0] = [p[1]] + p[3]

def p_cmds_single(p):
    '''cmds : cmd PONTO'''
    p[0] = [p[1]]

def p_cmd_set(p):
    '''cmd : SET ID IGUAL_SIMPLES valor'''
    nome = p[2]
    valor = p[4]
    if nome not in variaveis and nome not in dispositivos:
        variaveis[nome] = 'int'
        declaracoes.append(f'    int {nome} = {valor};')
        p[0] = f'    /* variável {nome} declarada no início */'
    else:
        p[0] = f'    {nome} = {valor};'


def p_cmd_ligar(p):
    '''cmd : LIGAR ID'''
    p[0] = f'    ligar("{p[2]}");'

def p_cmd_desligar(p):
    '''cmd : DESLIGAR ID'''
    p[0] = f'    desligar("{p[2]}");'

def p_cmd_alerta_simples(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING FECHA_PAREN ID'''
    p[0] = f'    alerta("{p[6]}", "{p[4]}");'

def p_cmd_alerta_obs(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING VIRGULA ID FECHA_PAREN ID'''
    msg = p[4]
    obs_name = p[6]
    device_name = p[8]
    if obs_name in variaveis:
        p[0] = f'    alerta_com_valor("{device_name}", "{msg}", {obs_name});'
    else:
        print(f"Aviso: Observation '{obs_name}' não definida. Usando 0.")
        p[0] = f'    alerta_com_valor("{device_name}", "{msg}", 0);'

def p_cmd_if(p):
    '''cmd : SE condicao ENTAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }}'

def p_cmd_if_else(p):
    '''cmd : SE condicao ENTAO cmd SENAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }} else {{\n{p[6]}\n    }}'

def p_cmd_alerta_broadcast(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING FECHA_PAREN PARA TODOS DOIS_PONTOS namedevice_list'''
    msg = p[4]
    devices = p[9]
    lines = []
    for dev in devices:
        lines.append(f'    alerta("{dev}", "{msg}");')
    p[0] = '\n'.join(lines)

def p_namedevice_list_multiple(p):
    '''namedevice_list : ID VIRGULA namedevice_list'''
    p[0] = [p[1]] + p[3]

def p_namedevice_list_single(p):
    '''namedevice_list : ID'''
    p[0] = [p[1]]

def p_condicao_simples(p):
    '''condicao : ID operador valor'''
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_condicao_dupla(p):
    '''condicao : ID operador valor ELOGICO condicao'''
    p[0] = f'({p[1]} {p[2]} {p[3]}) && ({p[5]})'

def p_operador(p):
    '''operador : MAIOR
                | MENOR
                | MAIORIGUAL
                | MENORIGUAL
                | IGUAL
                | DIFERENTE'''
    p[0] = p[1]

def p_valor(p):
    '''valor : NUM
             | ID'''
    if isinstance(p[1], int):
        p[0] = str(p[1])
    else:
        if p[1] == 'TRUE':
            p[0] = '1'
        elif p[1] == 'FALSE':
            p[0] = '0'
        else:
            p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe no final do input")

parser = yacc.yacc()
