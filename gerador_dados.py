import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def gerar_dados():
    np.random.seed(42)
    random.seed(42)
    
    # Criar pasta data se não existir
    os.makedirs('data', exist_ok=True)

    # 1. Produtos
    produtos = pd.DataFrame([
        {'id_produto': 'P001', 'nome_produto': 'Mouse Gamer Genérico', 'categoria': 'Acessórios', 'custo_unitario': 18.00},
        {'id_produto': 'P002', 'nome_produto': 'Teclado Mecânico RGB', 'categoria': 'Acessórios', 'custo_unitario': 85.00},
        {'id_produto': 'P003', 'nome_produto': 'Monitor 24" IPS', 'categoria': 'Monitores', 'custo_unitario': 450.00},
        {'id_produto': 'P004', 'nome_produto': 'Notebook Pro SSD', 'categoria': 'Computadores', 'custo_unitario': 2800.00},
        {'id_produto': 'P005', 'nome_produto': 'Cabo HDMI 2m', 'categoria': 'Cabos', 'custo_unitario': 8.00},
    ])
    produtos.to_csv('data/produtos.csv', index=False)
    
    # Precos de Venda (apenas para uso interno na geracao)
    # P001: 45.00 (Lucro alto relativo, mas vai ter volume no Online com alto custo)
    # P002: 199.00
    # P003: 799.00
    # P004: 4500.00 (Lucro bruto de 1700 - alta margem)
    # P005: 25.00
    precos = {'P001': 45.00, 'P002': 199.00, 'P003': 799.00, 'P004': 4500.00, 'P005': 25.00}

    # 2. Clientes (Pareto: 20 clientes gerando muito lucro)
    clientes_lista = []
    for i in range(1, 101):
        if i <= 20: # 20% Top
            clientes_lista.append({'id_cliente': f'C{i:03d}', 'nome': f'Empresa VIP {i}', 'segmento': 'Corporativo'})
        else:
            clientes_lista.append({'id_cliente': f'C{i:03d}', 'nome': f'Cliente Individual {i}', 'segmento': 'Individual'})
            
    clientes = pd.DataFrame(clientes_lista)
    clientes.to_csv('data/clientes.csv', index=False)

    # 3. Custos Logísticos e Marketing
    custos_logisticos = pd.DataFrame([
        {'canal': 'Online', 'custo_logistico_unitario': 15.00}, # Alto custo logístico
        {'canal': 'Fisico', 'custo_logistico_unitario': 2.00}
    ])
    custos_logisticos.to_csv('data/custos_logisticos.csv', index=False)

    marketing = pd.DataFrame([
        {'canal': 'Online', 'custo_marketing_percentual': 0.12}, # 12% da receita vai para marketing
        {'canal': 'Fisico', 'custo_marketing_percentual': 0.03}
    ])
    marketing.to_csv('data/marketing.csv', index=False)

    # 4. Vendas (Cenário: Volume sobe, Lucro cai nos últimos 6 meses)
    # Meses: Jan a Jun 2023
    vendas = []
    id_venda = 1
    
    # Lógica:
    # Mês 1: Boas vendas de Notebooks Físico (Alto Lucro)
    # Mês 6: Altíssimas vendas de Mouse/Cabo Online (Alto Volume, Lucro Quase Zero ou Negativo, Derrubando Lucro Total)
    
    meses_info = [
        {'mes': 1, 'ano': 2023, 'dias': 31, 'vol_base': 100, 'peso_online': 0.3, 'peso_notebook': 0.5},
        {'mes': 2, 'ano': 2023, 'dias': 28, 'vol_base': 120, 'peso_online': 0.4, 'peso_notebook': 0.4},
        {'mes': 3, 'ano': 2023, 'dias': 31, 'vol_base': 150, 'peso_online': 0.5, 'peso_notebook': 0.3},
        {'mes': 4, 'ano': 2023, 'dias': 30, 'vol_base': 200, 'peso_online': 0.6, 'peso_notebook': 0.2},
        {'mes': 5, 'ano': 2023, 'dias': 31, 'vol_base': 250, 'peso_online': 0.7, 'peso_notebook': 0.1},
        {'mes': 6, 'ano': 2023, 'dias': 30, 'vol_base': 350, 'peso_online': 0.85, 'peso_notebook': 0.05}
    ]

    for m in meses_info:
        # Puxando clientes corporativos para Notebooks para garantir os 20% -> 70% lucro
        for _ in range(m['vol_base']):
            canal = 'Online' if random.random() < m['peso_online'] else 'Fisico'
            
            # Escolha de produto
            rand_prod = random.random()
            if rand_prod < m['peso_notebook']: # Alta chance de Notebook e Monitor no inicio
                prod_id = random.choice(['P004', 'P004', 'P003'])
            else:
                prod_id = random.choice(['P001', 'P001', 'P005', 'P002']) # Mouse e Cabo
            
            # Se for Notebook/Monitor alto valor, grande chance de ser Cliente VIP Corporativo e Físico (historicamente lucro maior)
            if prod_id in ['P003', 'P004']:
                cliente_id = random.choice([f'C{i:03d}' for i in range(1, 21)]) # Top 20
                qtd = random.randint(1, 5) # Compram em volume
            else:
                cliente_id = random.choice([f'C{i:03d}' for i in range(21, 101)])
                qtd = random.randint(1, 2)
                
            dia = random.randint(1, m['dias'])
            data_venda = datetime(m['ano'], m['mes'], dia).strftime('%Y-%m-%d')
            
            vendas.append({
                'id_venda': id_venda,
                'data': data_venda,
                'id_produto': prod_id,
                'id_cliente': cliente_id,
                'canal': canal,
                'quantidade': qtd,
                'preco_unitario': precos[prod_id]
            })
            id_venda += 1

    df_vendas = pd.DataFrame(vendas)
    df_vendas.to_csv('data/vendas.csv', index=False)
    
    print(f"Dados gerados com sucesso na pasta 'data/'!")
    print(f"Total de vendas geradas: {len(df_vendas)}")

if __name__ == "__main__":
    gerar_dados()
