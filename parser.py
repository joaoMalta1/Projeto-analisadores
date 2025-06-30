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
    '''device : DISPOSITIVO DOIS_PONTOS ABRE_CHAVES NAMEDEVICE VIRGULA OBSERVATION FECHA_CHAVES'''
    dispositivos.add(p[4]) # namedevice
    # Você também pode querer armazenar p[6] (observation) se for necessário para verificações semânticas posteriores ou geração de código.
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
    # mude IGUAL para IGUAL_SIMPLES ou o nome que você usou para '='
    '''cmd : SET OBSERVATION IGUAL_SIMPLES valor'''
    nome = p[2]
    valor = p[4]
    if nome not in variaveis:
        # Assumindo que os valores de 'observation' são tratados como variáveis, e seu tipo depende do valor atribuído
        if isinstance(valor, int):
            variaveis[nome] = 'int'
            p[0] = f'    int {nome} = {valor};'
        elif isinstance(valor, bool):
            variaveis[nome] = 'bool'
            # Em C, booleano pode ser representado como int (0 ou 1)
            c_val = 1 if valor else 0
            p[0] = f'    int {nome} = {c_val};'
    else:
        p[0] = f'    {nome} = {valor};' # Isso assume consistência de tipo, você pode querer adicionar uma verificação de tipo aqui

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
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING VIRGULA OBSERVATION FECHA_PAREN NAMEDEVICE'''
    msg = p[4]
    obs_name = p[6] # Nome da observation
    device_name = p[8]

    # Recuperar o valor da observation de 'variaveis'
    # Você precisará garantir que 'variaveis' contenha o valor atual de 'obs_name'.
    # Para simplificar, assumindo que é um int aqui, mas você pode precisar de manipulação de tipo mais complexa.
    if obs_name in variaveis:
        # Em um compilador real, você obteria o valor atual de uma tabela de símbolos ou similar.
        # Para este parser, estamos apenas gerando código que usa o nome da variável.
        p[0] = f'    alerta_com_valor("{device_name}", "{msg}", {obs_name});'
    else:
        # Lidar com erro: observation não definida, ou assumir um padrão (ex: 0 conforme PDF para indefinido) [cite: 43]
        print(f"Aviso: Observation '{obs_name}' usada em alerta antes de ser definida. Assumindo 0.")
        p[0] = f'    alerta_com_valor("{device_name}", "{msg}", 0);'

def p_cmd_if(p):
    '''cmd : SE condicao ENTAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }}'

def p_cmd_if_else(p):
    '''cmd : SE condicao ENTAO cmd SENAO cmd'''
    p[0] = f'    if ({p[2]}) {{\n{p[4]}\n    }} else {{\n{p[6]}\n    }}'

def p_condicao_simples(p):
    '''condicao : OBSERVATION operador valor''' # Alterado NAMEDEVICE para OBSERVATION
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_condicao_dupla(p):
    '''condicao : OBSERVATION operador valor ELOGICO condicao''' # Alterado NAMEDEVICE para OBSERVATION
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

# Adicione esta nova regra CMD
def p_cmd_alerta_broadcast(p):
    '''cmd : ENVIAR ALERTA ABRE_PAREN STRING FECHA_PAREN PARA TODOS DOIS_PONTOS namedevice_list'''
    msg = p[4]
    devices = p[9] # Será uma lista de namedevices da regra namedevice_list
    code_lines = []
    for device in devices:
        code_lines.append(f'    alerta("{device}", "{msg}");')
    p[0] = '\n'.join(code_lines)

# Regra auxiliar para analisar uma lista de namedevices separada por vírgula
def p_namedevice_list_multiple(p):
    '''namedevice_list : NAMEDEVICE VIRGULA namedevice_list'''
    p[0] = [p[1]] + p[3]

def p_namedevice_list_single(p):
    '''namedevice_list : NAMEDEVICE'''
    p[0] = [p[1]]

# Constrói o parser
parser = yacc.yacc()

