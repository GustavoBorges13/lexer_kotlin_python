# main.py
import sys
import os
from .lexer import Lexer
from .token_stream import TokenStream
from .parser_kotlin import Parser

def analisar_codigo(nome_arquivo, source_text):
    """
    Executa o Lexer (imprime tokens) e em seguida executa o Parser (imprime AST / erros).
    """
    print(f"\n{'='*60}")
    print(f"PROCESSANDO: {nome_arquivo}")
    print(f"{'='*60}")
    
    # --- Passo 1: lexar e mostrar tokens (sem consumir o input permanentemente) ---
    lexer_for_print = Lexer(source_text)
    tokens = lexer_for_print.tokenize()
    for t in tokens:
        print(t)
    print("\n\n\nanalise lexica finalizada\n\n\n")
    
    # --- Passo 2: parsear (usamos um novo lexer/tokenstream para começar do início) ---
    lexer_for_parse = Lexer(source_text)
    ts = TokenStream(lexer_for_parse)
    parser = Parser(ts)
    ast = parser.parse()
    
    print(f"{'-'*60}")
    print("AST (sumário):")
    # imprimir de forma resumida (evita dumps gigantes)
    import json
    print(json.dumps(ast, indent=2, ensure_ascii=False))
    if parser.errors:
        print(f"{'-'*60}")
        print("Erros sintáticos encontrados:")
        for e in parser.errors:
            print(e)
    else:
        print(f"{'-'*60}")
        print("Parsing finalizado sem erros sintáticos detectados.")
    
    print(f"{'-'*60}")
    print(f"Análise finalizada para '{nome_arquivo}'.")

def carregar_arquivo(caminho_usuario):
    """
    Tenta localizar e ler o arquivo, resolvendo caminhos relativos e absolutos.
    """
    caminho_absoluto = os.path.abspath(caminho_usuario)
    
    if not os.path.exists(caminho_absoluto):
        print(f"\nERRO: O arquivo '{caminho_usuario}' não foi encontrado.")
        print(f"   Caminho buscado: {caminho_absoluto}")
        return

    try:
        with open(caminho_absoluto, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
            analisar_codigo(caminho_usuario, codigo_fonte)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

def exibir_ajuda():
    print("\nERRO: Nenhum arquivo de entrada foi especificado.")
    print("-" * 50)
    print("MODO DE USO:")
    print("   python -m LexerProject.main <arquivo1.kt> [arquivo2.kt ...]")
    print("\nEXEMPLOS:")
    print("   1. Rodar um arquivo na mesma pasta:")
    print("      python -m LexerProject.main teste.kt")
    print("\n   2. Rodar múltiplos arquivos:")
    print("      python -m LexerProject.main teste.kt outro.kt")
    print("\n   3. Rodar arquivo em outro diretório (Caminho Absoluto):")
    if os.name == 'nt': # Windows
        print(r"      python -m LexerProject.main C:\Users\user\Downloads\teste.kt")
    else: # Linux/Mac
        print("      python -m LexerProject.main /home/user/Downloads/teste.kt")
    print("-" * 50)

if __name__ == "__main__":
    arquivos = sys.argv[1:]

    if not arquivos:
        exibir_ajuda()
        sys.exit(1)

    for arquivo in arquivos:
        carregar_arquivo(arquivo)
