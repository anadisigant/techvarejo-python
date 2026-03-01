import pandas as pd

def carregar_dados():
    vendas = pd.read_csv('data/vendas.csv')
    produtos = pd.read_csv('data/produtos.csv')
    clientes = pd.read_csv('data/clientes.csv')
    custos_log = pd.read_csv('data/custos_logisticos.csv')
    mkt = pd.read_csv('data/marketing.csv')
    
    # Merge everything
    df = vendas.merge(produtos, on='id_produto')
    df = df.merge(clientes, on='id_cliente')
    df = df.merge(custos_log, on='canal')
    df = df.merge(mkt, on='canal')
    
    # Calcular Receita
    df['receita'] = df['preco_unitario'] * df['quantidade']
    
    # Formula dada:
    # lucro = (preco_unitario - custo_unitario - custo_logistico_unitario) * quantidade - (preco_unitario * quantidade * custo_marketing_percentual)
    df['lucro'] = (df['preco_unitario'] - df['custo_unitario'] - df['custo_logistico_unitario']) * df['quantidade'] - (df['preco_unitario'] * df['quantidade'] * df['custo_marketing_percentual'])
    
    df['data'] = pd.to_datetime(df['data'])
    df['mes_ano'] = df['data'].dt.to_period('M').astype(str)
    
    return df

if __name__ == '__main__':
    df = carregar_dados()
    print(f"Total Vendas: {len(df)}")
    print("\nMétrica 1 - Evolução Volume vs Lucro por Mês:")
    resumo_mes = df.groupby('mes_ano').agg({'quantidade': 'sum', 'lucro': 'sum', 'receita': 'sum'})
    print(resumo_mes)
    
    print("\nMétrica 2 - Lucro por Canal:")
    print(df.groupby('canal')['lucro'].sum())
    
    print("\nMétrica 3 - Pareto Clientes (Top 20%):")
    lucro_por_cliente = df.groupby('id_cliente')['lucro'].sum().sort_values(ascending=False)
    lucro_total = df['lucro'].sum()
    lucro_top_20 = lucro_por_cliente.head(20).sum()
    print(f"Lucro Total: {lucro_total:.2f}")
    print(f"Lucro Top 20 (20%): {lucro_top_20:.2f}")
    print(f"Percentual Lucro Top 20: {(lucro_top_20/lucro_total)*100:.2f}%")
    
    print("\nMétrica 4 - Produto mais vendido vs mais lucrativo:")
    print("Mais vendido (Quantidade):")
    print(df.groupby('nome_produto')['quantidade'].sum().sort_values(ascending=False))
    print("\nMais lucrativo:")
    print(df.groupby('nome_produto')['lucro'].sum().sort_values(ascending=False))
