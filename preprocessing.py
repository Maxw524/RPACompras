import pandas as pd

def limpar_dados(df):
    # Limpeza dos preços
    df['Preço'] = df['Preço'].replace({'R\$': '', '.': ''}, regex=True).astype(float)
    
    # Limpeza das avaliações
    df['Avaliação'] = df['Avaliação'].apply(lambda x: float(x.split()[0]) if x != "Sem Avaliação" else 0.0)
    
    # Conversão das categorias em valores numéricos
    df['Categoria'] = df['Categoria'].map({
        'Mercado Livre': 0, 'Amazon': 1, 'Magalu': 2, 'Casas Bahia': 3
    })
    
    return df
