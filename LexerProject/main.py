import sys
import os
from .lexer import Lexer
from .token_stream import TokenStream

def analisar_codigo(nome_arquivo, source_text):
    """
    Executa o Lexer para um conteúdo de texto específico.
    """
    print(f"\n{'='*60}")
    print(f"PROCESSANDO: {nome_arquivo}")
    print(f"{'='*60}")
    
    lexer = Lexer(source_text)
    ts = TokenStream(lexer)
    
    tokens_encontrados = 0
    
    while True:
        try:
            t = ts.next()
            print(t)
            tokens_encontrados += 1
            if t.tipo == "EOF":
                break
        except Exception as e:
            # Captura erros graves que escaparam do modo pânico
            print(f"ERRO FATAL: {e}")
            break
            
    print(f"{'-'*60}")
    print(f"Análise finalizada para '{nome_arquivo}'.")

def carregar_arquivo(caminho_usuario):
    """
    Tenta localizar e ler o arquivo, resolvendo caminhos relativos e absolutos.
    """
    # Transforma o caminho passado (ex: "../teste.kt" ou "C:/Users/...") em absoluto
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
    """
    Mostra como usar o programa caso nenhum argumento seja passado.
    """
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
    # Exemplo adaptativo para Windows ou Linux
    if os.name == 'nt': # Windows
        print(r"      python -m LexerProject.main C:\Users\user\Downloads\teste.kt")
    else: # Linux/Mac
        print("      python -m LexerProject.main /home/user/Downloads/teste.kt")
    print("-" * 50)

if __name__ == "__main__":
    # sys.argv[0] é o nome do script.
    # sys.argv[1:] são os argumentos passados pelo usuário.
    arquivos = sys.argv[1:]

    if not arquivos:
        exibir_ajuda()
        sys.exit(1) # Sai do programa indicando erro

    # Itera sobre todos os arquivos passados no comando
    for arquivo in arquivos:
        carregar_arquivo(arquivo)