import tkinter as tk
from tkinter import ttk
from layout import criar_layout
from funcionalidades import buscar_mercadolivre_api
from pdf_utils import gerar_orcamento_pdf
import tkinter as tk
from layout import criar_layout

def main():
    root = tk.Tk()
    root.title("Gerador de Orçamento")
    root.geometry("1500x850")
    root.config(bg="#F9F9F9")

    # Criar o layout
    frame_left, frame_right, entry_produto, tree_produtos, tree_orcamento, entry_solicitacao_numero, entry_solicitacao_data, entry_solicitante, entry_comprador, entry_justificativa, btn_buscar, btn_adicionar, btn_gerar_orcamento = criar_layout(root)

    # Aqui você pode adicionar as funções e lógica dos botões, como buscar produtos, gerar orçamento, etc.

    root.mainloop()

if __name__ == "__main__":
    main()
