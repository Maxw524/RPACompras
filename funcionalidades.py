import requests
from collections import defaultdict
from tkinter import messagebox
import webbrowser
import pandas as pd

# Função para corrigir links incompletos
def corrigir_link(link, dominio):
    if not link.startswith("http"):
        return f"{dominio}{link}"
    return link

# Função para buscar produtos no Mercado Livre usando a API com filtro específico
def buscar_mercadolivre_api(produto, max_results=100):
    url_base = f"https://api.mercadolibre.com/sites/MLB/search?q={produto}"
    produtos = []
    offset = 0  # Paginação
    palavras_chave = set(produto.lower().split())  # Palavras do termo buscado

    while len(produtos) < max_results:
        url = f"{url_base}&offset={offset}&limit=50"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se houve erro na resposta
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para Mercado Livre API: {e}")
            break

        data = response.json()
        dominio = "https://www.mercadolivre.com.br"
        for item in data.get('results', []):
            nome = item['title']
            preco = item['price']
            link = corrigir_link(item['permalink'], dominio)
            descricao = item.get('description', 'Sem Descrição')
            fornecedor = item.get('seller', {}).get('nickname', 'Fornecedor desconhecido')
            avaliacao = item.get('rating', 'Sem Avaliação')
            categoria = "Mercado Livre"

            # Filtro para verificar se o título contém todas as palavras-chave
            palavras_titulo = set(nome.lower().split())
            if palavras_chave.issubset(palavras_titulo):
                produtos.append([nome, preco, descricao, fornecedor, avaliacao, categoria, link])

            if len(produtos) >= max_results:
                break

        if not data.get('results'):
            break

        offset += 50  # Incrementa a página

    return produtos

# Função para abrir o link no navegador
def abrir_link(url):
    webbrowser.open_new(url)  # Usar open_new para garantir que abre em uma nova aba ou janela do navegador

# Função para exibir os resultados na interface gráfica
def exibir_resultados(entry_produto, tree_produtos):
    produto = entry_produto.get()

    if not produto:
        messagebox.showwarning("Entrada Inválida", "Por favor, digite um produto para pesquisar.")
        return

    produtos = buscar_mercadolivre_api(produto)

    if not produtos:
        messagebox.showinfo("Nenhum Produto", "Nenhum produto encontrado.")
        return

    # Limpa os itens existentes na treeview
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)

    # Organiza os produtos em um dataframe
    df = pd.DataFrame(produtos, columns=["Nome", "Preço", "Descrição", "Fornecedor", "Avaliação", "Categoria", "Link"])

    # Ordena os produtos mais baratos
    df_mais_baratos = df.nsmallest(3, "Preço")

    # Exibe os produtos mais baratos
    tree_produtos.insert('', 'end', values=("3 Mais Baratos", "", "", "", "", "", ""), tags=("titulo",))
    for _, row in df_mais_baratos.iterrows():
        # Ajuste: Insira os valores na ordem correta das colunas no tree_produtos
        item = tree_produtos.insert('', 'end', values=(row["Nome"], row["Preço"], row["Fornecedor"], row["Link"]))
        tree_produtos.tag_bind(item, "<Button-1>", lambda event, url=row['Link']: abrir_link(url))

    # Exibe os produtos restantes
    df_restante = df[~df.index.isin(df_mais_baratos.index)]
    tree_produtos.insert('', 'end', values=("Produtos Restantes", "", "", "", "", "", ""), tags=("titulo",))
    for _, row in df_restante.iterrows():
        # Ajuste: Insira os valores na ordem correta das colunas no tree_produtos
        item = tree_produtos.insert('', 'end', values=(row["Nome"], row["Preço"], row["Fornecedor"], row["Link"]))
        tree_produtos.tag_bind(item, "<Button-1>", lambda event, url=row['Link']: abrir_link(url))
