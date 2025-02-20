import tkinter as tk
from fpdf import FPDF
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import filedialog
import funcionalidades  # Assumindo que você está importando as funções de funcionalidades.py
import pdf_utils  # Caso precise importar também para gerar o PDF
import webbrowser  # Para abrir links no navegador

def criar_layout(root):
    # Criar o frame principal
    frame_principal = tk.Frame(root, bg="#F9F9F9")
    frame_principal.pack(padx=0, pady=0, fill="both", expand=True)

    # Divisão em duas colunas: Solicitação e Produtos
    frame_left = tk.Frame(frame_principal, bg="#F9F9F9")
    frame_left.grid(row=0, column=0, padx=0, pady=0)

    frame_right = tk.Frame(frame_principal, bg="#F9F9F9")
    frame_right.grid(row=0, column=1, padx=40, pady=0)

    # Função para carregar e redimensionar a logo
    def carregar_logo():
        try:
            logo_path = "logo.png"  # Caminho para o arquivo da logo
            logo = Image.open(logo_path)
            nova_largura = 400
            altura_logo = int((nova_largura / logo.width) * logo.height)
            logo = logo.resize((nova_largura, altura_logo), Image.Resampling.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo)
            return logo_tk
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a logo: {e}")
            return None

    # Exibir a logo no topo esquerdo da janela principal
    logo_image = carregar_logo()
    if logo_image:  # Somente exibe se a logo foi carregada com sucesso
        label_logo = ttk.Label(root, image=logo_image, background="#F9F9F9")
        label_logo.image = logo_image  # Armazena a referência para evitar garbage collection
        label_logo.place(x=10, y=10, anchor="nw")

    # Campos dentro do frame_left
    label_solicitacao_numero = ttk.Label(frame_left, text="Número da Solicitação:")
    label_solicitacao_numero.grid(row=1, column=0, sticky="w", pady=15)
    entry_solicitacao_numero = ttk.Entry(frame_left, width=30)
    entry_solicitacao_numero.grid(row=1, column=1, pady=15)

    label_solicitacao_data = ttk.Label(frame_left, text="Data da Solicitação:")
    label_solicitacao_data.grid(row=2, column=0, sticky="w", pady=15)
    entry_solicitacao_data = DateEntry(frame_left, width=30, style="TEntry", date_pattern="dd/mm/yyyy")
    entry_solicitacao_data.grid(row=2, column=1, pady=15)

    label_solicitante = ttk.Label(frame_left, text="Solicitante:")
    label_solicitante.grid(row=3, column=0, sticky="w", pady=15)
    entry_solicitante = ttk.Entry(frame_left, width=80, style="TEntry")
    entry_solicitante.grid(row=3, column=1, pady=15)

    label_comprador = ttk.Label(frame_left, text="Comprador:")
    label_comprador.grid(row=4, column=0, sticky="w", pady=15)
    entry_comprador = ttk.Entry(frame_left, width=80, style="TEntry")
    entry_comprador.grid(row=4, column=1, pady=15)

    label_justificativa = ttk.Label(frame_left, text="Justificativa:")
    label_justificativa.grid(row=5, column=0, sticky="w", pady=15)
    entry_justificativa = ttk.Entry(frame_left, width=80, style="TEntry")
    entry_justificativa.grid(row=5, column=1, pady=15)

    # ---------------------------------------------------
    # Coluna dos Produtos (lado direito)
    # ---------------------------------------------------
    label_produto = ttk.Label(frame_right, text="Produto:")
    label_produto.grid(row=0, column=0, sticky="w", pady=15)
    entry_produto = ttk.Entry(frame_right, width=35, style="TEntry")
    entry_produto.grid(row=0, column=1, pady=15)

    # Árvore para exibir todos os produtos encontrados
    tree_produtos = ttk.Treeview(frame_right, columns=("Nome", "Preço", "Fornecedor", "Link"), show="headings")
    tree_produtos.heading("Nome", text="Nome")
    tree_produtos.heading("Preço", text="Preço")
    tree_produtos.heading("Fornecedor", text="Fornecedor")  # Coluna para o fornecedor
    tree_produtos.heading("Link", text="Link")  # Coluna para o link do produto
    tree_produtos.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

    # Botão para buscar produtos
    btn_buscar = ttk.Button(frame_right, text="Buscar Produtos", command=lambda: funcionalidades.exibir_resultados(entry_produto, tree_produtos))
    btn_buscar.grid(row=0, column=2, pady=15)
    # Função para abrir o link no navegador
    def abrir_link(event):
        # Obter o item selecionado na árvore
        item = tree_produtos.selection()
        if item:
            # Obter os valores do item selecionado
            item_values = tree_produtos.item(item)["values"]
            # O link está na quarta coluna (índice 3)
            link = item_values[3]
            # Verificar se o link não está vazio e abrir no navegador
            if link:
                webbrowser.open(link)
            else:
                messagebox.showwarning("Link inválido", "Este produto não possui um link válido.")

    # Vincule o evento de duplo clique na árvore tree_produtos para abrir o link
    tree_produtos.bind("<Double-1>", abrir_link)

    # Árvore para exibir produtos no orçamento
    tree_orcamento = ttk.Treeview(frame_right, columns=("Nome", "Preço", "Fornecedor", "Link"), show="headings")
    tree_orcamento.heading("Nome", text="Nome")
    tree_orcamento.heading("Preço", text="Preço")
    tree_orcamento.heading("Fornecedor", text="Fornecedor")
    tree_orcamento.heading("Link", text="Link")  # Coluna para o link do produto
    tree_orcamento.grid(row=4, column=0, columnspan=3, pady=15, sticky="nsew")

    # Função para adicionar um produto ao orçamento
    def adicionar_ao_orcamento():
        selected_item = tree_produtos.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um produto para adicionar ao orçamento.")
            return
        item_values = tree_produtos.item(selected_item)["values"]
        
        nome = item_values[0]    # Nome do produto
        preco = item_values[1]   # Preço do produto
        fornecedor = item_values[2]  # Fornecedor do produto
        link = item_values[3]    # Link do produto
        tree_orcamento.insert("", "end", values=(nome, preco, fornecedor, link))

    # Função para remover o produto ao dar um duplo clique
    def remover_do_orcamento(event):
        selected_item = tree_orcamento.selection()
        if not selected_item:
            return
        confirm = messagebox.askyesno("Remover Produto", "Tem certeza que deseja remover o produto selecionado?")
        if confirm:
            for item in selected_item:
                tree_orcamento.delete(item)

    # Vincule o evento de duplo clique para remover itens
    tree_orcamento.bind("<Double-1>", remover_do_orcamento)

    def gerar_orcamento():
        if not tree_orcamento.get_children():
            messagebox.showwarning("Orçamento Vazio", "Não há produtos no orçamento para gerar.")
            return

        data_solicitacao = entry_solicitacao_data.get_date()
        justificativa = entry_justificativa.get()
        comprador = entry_comprador.get()
        solicitante = entry_solicitante.get()
        numeroDaSolicitacao = entry_solicitacao_numero.get()

        try:
            pdf_utils.gerar_orcamento_pdf(tree_orcamento, data_solicitacao, justificativa, comprador, solicitante, numeroDaSolicitacao)
            messagebox.showinfo("PDF Gerado", "Orçamento gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro ao Gerar PDF", f"Erro ao gerar o PDF: {e}")

    # Botões para adicionar e gerar orçamento
    btn_adicionar = ttk.Button(frame_right, text="Adicionar ao Orçamento", command=adicionar_ao_orcamento)
    btn_adicionar.grid(row=3, column=0, columnspan=3, pady=15)

    btn_gerar_orcamento = ttk.Button(frame_right, text="Gerar Orçamento", command=gerar_orcamento)
    btn_gerar_orcamento.grid(row=5, column=0, columnspan=3, pady=15)

    # Retornar os widgets importantes
    return frame_left, frame_right, entry_produto, tree_produtos, tree_orcamento, entry_solicitacao_numero, entry_solicitacao_data, entry_solicitante, entry_comprador, entry_justificativa, btn_buscar, btn_adicionar, btn_gerar_orcamento
