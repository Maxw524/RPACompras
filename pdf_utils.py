import os
from fpdf import FPDF
from tkinter import filedialog, messagebox

def gerar_orcamento_pdf(tree_orcamento, data_solicitacao, justificativa, comprador, solicitante, numeroDaSolicitacao):
    if not tree_orcamento.get_children():
        raise ValueError("Não há produtos no orçamento para gerar.")
    
    class CustomPDF(FPDF):
        def header(self):
            logo_path = "C:/RpaCompras/img/logo.png"
            # Verificar se o arquivo de logo existe
            if os.path.exists(logo_path):
                self.image(logo_path, 10, 8, 33)  # Caminho correto da logo
            else:
                messagebox.showerror("Erro", f"O arquivo de logo '{logo_path}' não foi encontrado!")
                return

            self.set_font("Arial", style="B", size=12)  # Tamanho reduzido do cabeçalho
            self.cell(0, 10, "SOLICITAÇÃO DE COMPRAS", ln=True, align="C")
            self.ln(5)

    # Cria o PDF
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=9)  # Fonte ajustada para todo o conteúdo

    # Cabeçalho com a data da solicitação
    pdf.cell(0, 8, f"Data da Solicitação: {data_solicitacao.strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)
    # Numero da solicitação
    pdf.cell(0, 8, f"Numero Solicitação: {numeroDaSolicitacao}", ln=True)
    pdf.ln(5)

    # Adiciona o campo Justificativa
    pdf.cell(30, 8, "Solicitante:", border=1)
    pdf.multi_cell(0, 8, solicitante, border=1)

    # Adiciona o campo Justificativa
    pdf.cell(30, 8, "COMPRADOR:", border=1)
    pdf.multi_cell(0, 8, comprador, border=1)

    # Adiciona o campo Justificativa
    pdf.cell(30, 8, "JUSTIFICATIVA:", border=1)
    pdf.multi_cell(0, 8, justificativa, border=1)  # Usa multi_cell para justificar o texto de forma adequada

    pdf.ln(10)

    # Cabeçalho da tabela com colunas ajustadas
    pdf.set_font("Arial", size=8)  # Tamanho de fonte reduzido para o cabeçalho da tabela
    pdf.cell(20, 8, "Item", border=1, align="C")
    pdf.cell(70, 8, "Especificação", border=1, align="C")
    pdf.cell(10, 8, "Und", border=1, align="C")
    pdf.cell(10, 8, "Qtd", border=1, align="C")
    pdf.cell(15, 8, "Preço Unit.", border=1, align="C")
    pdf.cell(15, 8, "Preço Total", border=1, align="C")
    pdf.cell(0, 8, "Fornecedor", border=1, align="C", ln=True)

    total = 0  # Variável para armazenar o total

    # Preenche a tabela com os produtos
    for idx, item in enumerate(tree_orcamento.get_children(), start=1):
        item_values = tree_orcamento.item(item)["values"]

        # Verifica se há valores suficientes
        if len(item_values) < 3:
            continue  # Pular o item se não tiver o número esperado de valores

        nome, preco, fornecedor = item_values[0], item_values[1], item_values[2]

        try:
            preco = float(preco.replace("R$", "").replace(",", ".").strip())
        except ValueError:
            preco = 0  # Se o preço for inválido, assume-se zero

        # Preenche a linha da tabela
        pdf.cell(20, 8, str(idx), border=1, align="C")
        
        # Limita a quantidade de caracteres da "Especificação" para 30 caracteres
        nome = nome[:30]  # Limitar o nome a 30 caracteres (ajuste conforme necessário)

        # Exibe a especificação com a largura limitada
        pdf.cell(70, 8, nome, border=1, align="L")
        
        # Alinhamento à direita para as colunas: Un, Qtd, Preço Unit., Preço Total
        pdf.cell(10, 8, "Un", border=1, align="C")  # Unidade como exemplo
        pdf.cell(10, 8, "1", border=1, align="C")  # Quantidade como exemplo
        pdf.cell(15, 8, f"R${preco:.2f}", border=1, align="C")
        pdf.cell(15, 8, f"R${preco:.2f}", border=1, align="C")

        # Para o fornecedor, usamos uma largura maior
        pdf.cell(0, 8, fornecedor, border=1, align="L", ln=True)  # Ajusta a posição para a coluna "Fornecedor"

        total += preco  # Adiciona o preço de cada item ao total
        
    # Total
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=9)  # Fonte ajustada para o total
    pdf.cell(30, 8, "Valor Total", border=1, align="R")
    pdf.cell(20, 8, f"R${total:.2f}", border=1, align="C", ln=True)

    # Campo de assinatura 
    pdf.ln(35)  # Aumenta o espaço antes da área de assinatura
    pdf.ln(5)

    # Criar três linhas de 7 cm para assinaturas lado a lado com um espaço entre elas
    pdf.cell(60, 10, "_________________________________________________________", align="C")
    pdf.cell(10, 10, "")  # Espaço entre a primeira e a segunda linha (ajuste o valor conforme necessário)
    pdf.cell(60, 10, "_________________________________________________________", align="C")
    pdf.cell(10, 10, "")  # Espaço entre a segunda e a terceira linha (ajuste o valor conforme necessário)
    pdf.cell(60, 10, "_________________________________________________________", align="C")
    pdf.ln(5)  # Dá um pequeno espaço depois das três linhas de assinatura

    # Criar os títulos para cada assinatura
    pdf.cell(60, 10, "Assinatura do Solicitante", align="C")
    pdf.cell(60, 10, "Assinatura da Gerência Administrativa", align="C")
    pdf.cell(60, 10, "Assinatura do Diretor Administrativo", align="C")
    pdf.ln(10)

    # Rodapé com fornecedor e link (pequena fonte)
    pdf.set_font("Arial", size=5)  # Fonte pequena para o rodapé
    pdf.cell(0, 5, "Fornecedores e Links:", ln=True)

    # Adiciona os fornecedores e links no rodapé
    for item in tree_orcamento.get_children():
        item_values = tree_orcamento.item(item)["values"]
        
        # Verifica se há o fornecedor e o link antes de tentar acessar
        if len(item_values) < 4:  # Certifique-se de que há pelo menos 4 colunas: nome, preço, fornecedor, link
            continue  # Pula o item se não houver link ou fornecedor

        fornecedor = item_values[2]  # Fornecedor
        link = item_values[3]  # Link do produto

        # Cria a linha completa com fornecedor e link
        linha_completa = f"{fornecedor}: {link}"

        # Escreve o fornecedor e o link como uma única célula
        pdf.set_text_color(0, 0, 255)  # Define cor azul para o link (toda a linha)
        pdf.write(5, linha_completa, link)  # Define o texto clicável para toda a linha

        pdf.ln(4)  # Adiciona espaçamento entre as linhas
              
    # Salvar o PDF
    try:
        pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_file:
            return

        # Verifica se o arquivo já existe e pergunta ao usuário se deseja sobrescrever
        if os.path.exists(pdf_file):
            overwrite = messagebox.askyesno("Sobrescrever Arquivo", "O arquivo já existe. Deseja substituí-lo?")
            if not overwrite:
                return

            # Se o usuário confirmar, remove o arquivo antigo
            os.remove(pdf_file)

        # Salva o arquivo PDF
        pdf.output(pdf_file)
    except Exception as e:
        raise ValueError(f"Erro ao salvar o PDF: {e}")
