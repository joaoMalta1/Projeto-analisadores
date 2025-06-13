from lex import lexer
import re

codigo = '''
dispositivo: {Termometro, temperatura}
set temperatura = 40.
se temperatura > 30 entao ligar Termometro.
'''

lexer.input(codigo)

for token in lexer:
    print(token)

# texto = ""

# matches = re.findall(r'"[^"]+"', texto)
# print(matches)  # ['"abc"', '"123"']
