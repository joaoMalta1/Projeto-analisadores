from lex import lexer
from parser import parser
import sys
import io

# --- função auxiliar para “achatar” listas ---
def flatten(lst):
    flat = []
    for item in lst:
        if isinstance(item, list):
            flat.extend(flatten(item))
        elif item != '':
            flat.append(item)
    return flat

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py entrada.obsact saida.c")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with io.open(input_file, 'r', encoding='utf-8-sig') as f:
            code = f.read()
    except UnicodeDecodeError:
        print(f"Erro ao ler '{input_file}' (use UTF-8).")
        sys.exit(1)

    code = code.lstrip()

    # Parse e recupera o código gerado
    resultado = parser.parse(code, lexer=lexer)

    if resultado is None:
        print("Erro de sintaxe")
        sys.exit(1)

    # Achata o resultado (caso tenha listas dentro)
    resultado_flat = flatten(resultado)

    try:
        with io.open(output_file, 'w', encoding='utf-8') as f:
            for line in resultado_flat:
                f.write(line + '\n')
        print(f"{output_file} gerado com sucesso!")
    except Exception as e:
        print(f"Erro: {e} ao gerar arquivo .c")
        sys.exit(1)

if __name__ == '__main__':
    main()
