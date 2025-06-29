from parser import parser

codigo = '''
dispositivo: {Ventilador, temperatura}
set temperatura = 40.
se temperatura > 30 entao ligar Ventilador.
'''

parser.parse(codigo)
