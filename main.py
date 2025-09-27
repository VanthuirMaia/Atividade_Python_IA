import json
import os

ARQUIVO_PADRAO = "livros.json"

def cadastrar_livro():
    livro = {}
    livro['titulo'] = input("Digite o Titulo do Livro: ").strip()
    livro['autor'] = input("Digite o nome do Autor: ").strip()
    # validações simples
    while True:
        try:
            livro['ano_publicacao'] = int(input("Digite o ano de publicação: ").strip())
            break
        except ValueError:
            print("Ano inválido. Tente novamente (ex.: 2020).")
    while True:
        try:
            livro['preco_venda'] = float(input("Digite o preço de venda (ex.: 49.90): ").replace(",", ".").strip())
            break
        except ValueError:
            print("Preço inválido. Tente novamente.")
    return livro

def menu():
    print("\nMenu:")
    print("1 - Cadastrar Livro")
    print("2 - Listar Livros")
    print("3 - Salvar em arquivo")
    print("4 - Abrir de arquivo")
    print("0 - Sair")

def listar_livros(livros):
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("\n=== Lista de Livros ===")
    for i, l in enumerate(livros, start=1):
        print(f"{i}. {l.get('titulo','?')} — {l.get('autor','?')} "
              f"({l.get('ano_publicacao','?')}) | R$ {l.get('preco_venda',0):.2f}")

def pedir_caminho(padrao=ARQUIVO_PADRAO, acao="arquivo"):
    caminho = input(f"Digite o nome do {acao} (Enter para '{padrao}'): ").strip()
    return caminho or padrao

def salvar_livros(livros, arquivo=ARQUIVO_PADRAO):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(livros, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em '{arquivo}' ({len(livros)} registro(s)).")
    except Exception as e:
        print("Erro ao salvar:", e)

def carregar_livros(arquivo=ARQUIVO_PADRAO):
    if not os.path.exists(arquivo):
        print(f"Aviso: '{arquivo}' não existe. Iniciando com lista vazia.")
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if not isinstance(dados, list):
            print("Formato inválido no arquivo. Iniciando com lista vazia.")
            return []
        print(f"Arquivo '{arquivo}' carregado ({len(dados)} registro(s)).")
        return dados
    except json.JSONDecodeError:
        print("Erro: arquivo não está em JSON válido. Iniciando com lista vazia.")
        return []
    except Exception as e:
        print("Erro ao abrir:", e)
        return []

def main():
    # Auto-carrega se o arquivo padrão existir
    livros = carregar_livros(ARQUIVO_PADRAO) if os.path.exists(ARQUIVO_PADRAO) else []
    arquivo_atual = ARQUIVO_PADRAO

    opcao = -1
    while opcao != 0:
        try:
            menu()
            opcao = int(input("\nDigite a opção desejada: ").strip())
        except ValueError as ve:
            print("Erro:", ve)
            continue
        except Exception as e:
            print("Aconteceu algo inesperado:", e)
            continue

        if opcao == 1:
            livros.append(cadastrar_livro())
        elif opcao == 2:
            listar_livros(livros)
        elif opcao == 3:
            # salvar
            caminho = pedir_caminho(arquivo_atual, "arquivo para salvar")
            salvar_livros(livros, caminho)
            arquivo_atual = caminho
        elif opcao == 4:
            # abrir
            caminho = pedir_caminho(arquivo_atual, "arquivo para abrir")
            livros = carregar_livros(caminho)
            arquivo_atual = caminho
        elif opcao == 0:
            print("Programa sendo encerrado...")
            # auto-salvar no arquivo atual
            salvar_livros(livros, arquivo_atual)
        else:
            print("Opção inválida...")

if __name__ == "__main__":
    main()
