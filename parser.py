import ply.yacc as yacc
from lex import tokens

# Variáveis auxiliares
codigo_gerado = []
variaveis = {}  # guarda variáveis já declaradas
dispositivos = set()

# Cabeçalho padrão do programa em C
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
    codigo = cabecalho_c + p[2] + fim_c
    with open('saida.c', 'w') as f:
        f.write('\n'.join(codigo))
    print("✅ Código C gerado com sucesso em 'saida.c'.")

def p_devices_multiple(p):
    '''devices : device devices'''
    p[0] = [p[1]] + p[2]

def p_devices_single(p):
    '''devices : device'''
    p[0] = [p[1]]

def p_device_obs(p):
    '''device : DISPOSITIVO DOIS_PONTOS ABRE_CHAVES NAMEDEVICE VIRGULA NAMEDEVICE FECHA_CHAVES'''
    dispositivos.add(p[4])
    p[0] = None

def p_device_simple(p):
    '''device : DISPOSITIVO DOIS_PONTOS ABRE_CHAVES NAMEDEVICE FECHA_CHAVES'''
    dispositivos.add(p[4])
    p[0] = None

def p_cmds_multiple(p):
    '''cmds : cmd PONTO cmds'''
    p[0] = [p[1]] + p[3]

def p_cmds_single(p):
    '''cmds : cmd PONTO'''
    p[0] = [p[1]]

def p_cmd_set(p):
    '''cmd : SET NAMEDEVICE IGUAL NUM'''
    nome = p[2]
    valor = p[4]
    if nome not in variaveis:
        variaveis[nome] = 'int'
        p[0] = f'    int {nome} = {valor};'
    else:
        p[0] = f'    {nome} = {valor};'

def p_cmd_ligar(p):
    '''cmd : LIGAR NAMEDEVICE'''
    p[0] = f'    ligar("{p[2]}");'

def p_cmd_desligar(p):
    '''cmd : DESLIGAR NAMEDEVICE'''
    p[0] = f'    desligar("{p[2]}");'

def p_cmd_alerta_simples(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING FECHA_PAREN NAMEDEVICE'''
    p[0] = f'    alerta("{p[6]}", "{p[4]}");'

def p_cmd_alerta_obs(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING VIRGULA NAMEDEVICE FECHA_PAREN NAMEDEVICE'''
    p[0] = f'    alerta_com_valor("{p[8]}", "{p[4]}", {p[6]});'

def p_cmd_if(p):
    '''cmd : SE condicao ENTAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }}'

def p_cmd_if_else(p):
    '''cmd : SE condicao ENTAO cmd SENAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }} else {{\n{p[6]}\n    }}'

def p_condicao_simples(p):
    '''condicao : NAMEDEVICE operador valor'''
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_condicao_dupla(p):
    '''condicao : NAMEDEVICE operador valor ELOGICO condicao'''
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
             | BOOL'''
    p[0] = str(p[1])

def p_error(p):
    if p:
        print(f"❌ Erro de sintaxe em '{p.value}' (linha {p.lineno})")
    else:
        print("❌ Erro de sintaxe no final do input")

# Constrói o parser
parser = yacc.yacc()

