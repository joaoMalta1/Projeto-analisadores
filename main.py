from parser import parser
import sys
import io
from lex import lexer
from parser import parser, dispositivos, variaveis, codigo_gerado


def main():
    if len(sys.argv) != 3:
        print("python main.py: input.obsact  e gera saida.c\n")
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]

    try:
        with io.open(input, 'r', encoding='utf-8-sig') as f:
            codigo = f.read()
    except UnicodeDecodeError:
        print(f" erro ao ler '{input}' (use UTF-8).")
        sys.exit(1)

    #tira \t\n e outros caracteres do começo 
    codigo = codigo.lstrip()

    #limpa as listas antes de gerar o novo codigo
    dispositivos.clear()
    variaveis.clear()
    codigo_gerado.clear()

    #parser
    resultado = parser.parse(codigo, lexer=lexer)
    if resultado is None:
        print("erro de sintaxe")
        sys.exit(1)

    #escrever o codigo .c
    try:
        with io.open(output, 'w', encoding='utf-8') as f:
            f.write(resultado)
        print(f"{output} gerado com sucesso em ")
    except Exception as e:
        print(f"erro ao gerar {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
