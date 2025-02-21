import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import filedialog
import funcionalidades  # Supondo que as funções estejam neste arquivo
import pdf_utils  # Caso precise importar para gerar o PDF
import webbrowser  # Para abrir links no navegador
import os  # Para verificar a existência dos arquivos


def criar_layout(root):
    # Criar o frame principal
    frame_principal = tk.Frame(root, bg="#F9F9F9")
    frame_principal.pack(padx=0, pady=0, fill="both", expand=True)

    # Divisão em duas colunas: Solicitação e Produtos
    frame_left = tk.Frame(frame_principal, bg="#F9F9F9")
    frame_left.grid(row=0, column=0, padx=0, pady=0)

    frame_right = tk.Frame(frame_principal, bg="#F9F9F9")
    frame_right.grid(row=0, column=1, padx=40, pady=0)

    # Função para carregar o logo
    def carregar_logo():
        try:
            logo_path = "C:/RpaCompras/img/logo.png"  # Caminho absoluto
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"O arquivo de logo não foi encontrado: {logo_path}")
            logo = Image.open(logo_path)
            nova_largura = 400
            altura_logo = int((nova_largura / logo.width) * logo.height)
            logo = logo.resize((nova_largura, altura_logo), Image.Resampling.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo)
            return logo_tk
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a logo: {e}")
            return None

    # Exibir a logo
    logo_image = carregar_logo()
    if logo_image:
        label_logo = ttk.Label(root, image=logo_image, background="#F9F9F9")
        label_logo.image = logo_image
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
    tree_produtos.heading("Fornecedor", text="Fornecedor")
    tree_produtos.heading("Link", text="Link")
    tree_produtos.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

    # Campos para inserir produto manualmente
    label_nome_manual = ttk.Label(frame_right, text="Nome do Produto:")
    label_nome_manual.grid(row=2, column=0, sticky="w", pady=15)
    entry_nome_manual = ttk.Entry(frame_right, width=35, style="TEntry")
    entry_nome_manual.grid(row=2, column=1, pady=15)

    label_fornecedor_manual = ttk.Label(frame_right, text="Fornecedor:")
    label_fornecedor_manual.grid(row=3, column=0, sticky="w", pady=15)
    entry_fornecedor_manual = ttk.Entry(frame_right, width=35, style="TEntry")
    entry_fornecedor_manual.grid(row=3, column=1, pady=15)

    label_link_manual = ttk.Label(frame_right, text="Link / Celular (opcional):")
    label_link_manual.grid(row=4, column=0, sticky="w", pady=15)
    entry_link_manual = ttk.Entry(frame_right, width=35, style="TEntry")
    entry_link_manual.grid(row=4, column=1, pady=15)

    # Função para adicionar o produto manual ao orçamento
    def adicionar_produto_manual():
        nome = entry_nome_manual.get()
        fornecedor = entry_fornecedor_manual.get()
        link = entry_link_manual.get()

        if not nome or not fornecedor:
            messagebox.showwarning("Campos obrigatórios", "Por favor, preencha o nome e o fornecedor do produto.")
            return
        
        # Inserir o produto na árvore do orçamento
        tree_orcamento.insert("", "end", values=(nome, "", fornecedor, link))

        # Limpar os campos de entrada
        entry_nome_manual.delete(0, tk.END)
        entry_fornecedor_manual.delete(0, tk.END)
        entry_link_manual.delete(0, tk.END)

    # Função para adicionar produto da pesquisa ao orçamento
    def adicionar_ao_orcamento():
        selected_item = tree_produtos.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um produto para adicionar.")
            return
        
        item = tree_produtos.item(selected_item)
        produto = item["values"]

        # Adicionar ao orçamento
        tree_orcamento.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3]))

    # Árvore para exibir produtos no orçamento
    tree_orcamento = ttk.Treeview(frame_right, columns=("Nome", "Preço", "Fornecedor", "Link"), show="headings")
    tree_orcamento.heading("Nome", text="Nome")
    tree_orcamento.heading("Preço", text="Preço")
    tree_orcamento.heading("Fornecedor", text="Fornecedor")
    tree_orcamento.heading("Link", text="Link")
    tree_orcamento.grid(row=6, column=0, columnspan=3, pady=15, sticky="nsew")

    # Função para gerar orçamento (PDF)
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

    # Função para abrir o link ao dar duplo clique
    def abrir_link(event):
        item = tree_produtos.selection()
        if item:
            produto = tree_produtos.item(item)["values"]
            link = produto[3]  # O link está na quarta coluna
            if link:
                webbrowser.open(link)

    # Função para remover produto do orçamento ao dar duplo clique
    def remover_produto(event):
        item = tree_orcamento.selection()
        if item:
            tree_orcamento.delete(item)

    # Conectar eventos de duplo clique
    tree_produtos.bind("<Double-1>", abrir_link)
    tree_orcamento.bind("<Double-1>", remover_produto)

   # Botões para adicionar produto manual e adicionar ao orçamento
    btn_adicionar_ao_orcamento = ttk.Button(frame_right, text="Adicionar ao Orçamento", command=adicionar_ao_orcamento)
    btn_adicionar_ao_orcamento.grid(row=5, column=1, pady=15, sticky="ew")  # Alterado para usar a largura total
    
    btn_adicionar_manual = ttk.Button(frame_right, text="Adicionar Produto Manual", command=adicionar_produto_manual)
    btn_adicionar_manual.grid(row=5, column=2, pady=15, padx=10, sticky="ew")  # Ao lado do botão "Adicionar ao Orçamento"

    btn_gerar_orcamento = ttk.Button(frame_right, text="Gerar Orçamento", command=gerar_orcamento)
    btn_gerar_orcamento.grid(row=7, column=0, columnspan=3, pady=15)

    # Botão para buscar produtos
    btn_buscar = ttk.Button(frame_right, text="Buscar Produtos", command=lambda: funcionalidades.exibir_resultados(entry_produto, tree_produtos))
    btn_buscar.grid(row=0, column=2, pady=15)

    # Retornar os widgets importantes
    return frame_left, frame_right, entry_produto, tree_produtos, tree_orcamento, entry_solicitacao_numero, entry_solicitacao_data, entry_solicitante, entry_comprador, entry_justificativa, btn_buscar, btn_adicionar_ao_orcamento, btn_gerar_orcamento
