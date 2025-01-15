import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed



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
            avaliacao = item.get('rating', 'Sem Avaliação')
            categoria = "Mercado Livre"

            # Filtro para verificar se o título contém todas as palavras-chave
            palavras_titulo = set(nome.lower().split())
            if palavras_chave.issubset(palavras_titulo):
                produtos.append([nome, preco, avaliacao, categoria, link])

            if len(produtos) >= max_results:
                break

        if not data.get('results'):
            break

        offset += 50  # Incrementa a página

    return produtos

# Função para buscar produtos na Amazon
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def buscar_amazon(produto):
    url = f"https://www.amazon.com.br/s?k={produto}&crid=3RYLA7Z9NFU2I&sprefix=%2Caps%2C560&ref=nb_sb_ss_recent_1_0_recent"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para Amazon: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    produtos = []

    items = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in items:
        try:
            nome = item.h2.text.strip()
            preco = item.find('span', {'class': 'a-price-whole'}).text.strip()
            link = "https://www.amazon.com.br" + item.h2.a['href']
            avaliacao = item.find('span', {'class': 'a-icon-alt'}).text.strip() if item.find('span', {'class': 'a-icon-alt'}) else "Sem Avaliação"
            categoria = "Amazon"
            produtos.append([nome, preco, avaliacao, categoria, link])
        except AttributeError:
            continue

    return produtos

# Função para buscar produtos na OLX
def buscar_olx(produto):
    url = f"https://www.olx.com.br/items/q-{produto.replace(' ', '-')}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para OLX: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    produtos = []

    items = soup.find_all('li', {'class': 'sc-16mf7lz-1'})
    for item in items:
        try:
            nome = item.find('h2').text.strip()
            preco = item.find('span', {'class': 'sc-1owow2i-1'}).text.strip()
            link = item.a['href']
            avaliacao = "Sem Avaliação"
            categoria = "OLX"
            produtos.append([nome, preco, avaliacao, categoria, link])
        except AttributeError:
            continue

    return produtos

# Função para abrir o link no navegador
def abrir_link(url):
    webbrowser.open(url)

# Função para buscar produtos de acordo com o site escolhido
def buscar_produtos_site_especifico(produto, site):
    if site == "Mercado Livre":
        return buscar_mercadolivre_api(produto)
    elif site == "Amazon":
        return buscar_amazon(produto)
    elif site == "OLX":
        return buscar_olx(produto)
    else:
        return []

# Função para exibir os resultados na interface gráfica
def exibir_resultados():
    produto = entry_produto.get()
    site = site_combobox.get()

    if not produto:
        messagebox.showwarning("Entrada Inválida", "Por favor, digite um produto para pesquisar.")
        return

    produtos = buscar_produtos_site_especifico(produto, site)

    if not produtos:
        messagebox.showinfo("Nenhum Produto", "Nenhum produto encontrado.")
        return

    for item in tree.get_children():
        tree.delete(item)

    df = pd.DataFrame(produtos, columns=["Nome", "Preço", "Avaliação", "Categoria", "Link"])
    df_mais_baratos = df.nsmallest(3, "Preço")

    tree.insert('', 'end', values=("3 Mais Baratos", "", "", "", ""), tags=("titulo",))
    for _, row in df_mais_baratos.iterrows():
        tree.insert('', 'end', values=row.tolist(), tags=("mais_barato",))

    df_restante = df[~df.index.isin(df_mais_baratos.index)]
    tree.insert('', 'end', values=("Produtos Restantes", "", "", "", ""), tags=("titulo",))
    for _, row in df_restante.iterrows():
        tree.insert('', 'end', values=row.tolist())

# Criar a janela principal
root = tk.Tk()
root.title("Busca de Produtos")

label_produto = tk.Label(root, text="Digite o nome do produto:")
label_produto.pack(padx=10, pady=5)

entry_produto = tk.Entry(root, width=50)
entry_produto.pack(padx=10, pady=5)

label_site = tk.Label(root, text="Escolha o site:")
label_site.pack(padx=10, pady=5)

site_choices = ["Mercado Livre", "Amazon", "OLX"]
site_combobox = ttk.Combobox(root, values=site_choices, state="readonly")
site_combobox.set("Mercado Livre")
site_combobox.pack(padx=10, pady=5)

button_buscar = tk.Button(root, text="Buscar", command=exibir_resultados)
button_buscar.pack(padx=10, pady=10)

cols = ("Nome", "Preço", "Avaliação", "Categoria", "Link")
tree = ttk.Treeview(root, columns=cols, show="headings", height=10)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(padx=10, pady=10)

def on_item_select(event):
    item = tree.selection()
    if item:
        link = tree.item(item, "values")[4]
        abrir_link(link)

tree.bind("<Double-1>", on_item_select)

root.mainloop()
