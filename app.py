import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import analise

# Configuração da página
st.set_page_config(
    page_title="TechVarejo S.A. - Dashboard SAD",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização Global Dinâmica (Suporta Dark/Light mode nativamente)
st.markdown("""
    <style>
    /* Ajustes pontuais de espaçamento e tipografia */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-weight: 600 !important;
    }
    
    /* Highlight elements sem quebrar contraste */
    .highlight {
        color: var(--text-color);
        font-weight: bold;
        background-color: var(--primary-color);
        padding: 2px 5px;
        border-radius: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# Função para métricas estilo "Card" elegante
def render_metric_card(title, value, icon="📈", border_color="#3b82f6"):
    st.markdown(f"""
    <div style="
        background-color: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid var(--faded-text-10);
        border-left: 5px solid {border_color};
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    ">
        <div style="color: var(--text-color); font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0.7;">
            {icon} &nbsp;{title}
        </div>
        <div style="color: var(--text-color); font-size: 2.2rem; font-weight: 700; font-family: 'Inter', sans-serif;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.title("TechVarejo S.A. - Painel Estratégico")
st.markdown("Bem-vindo ao painel de inteligência de negócios. Acompanhe os principais indicadores e tome decisões baseadas em dados.")
st.divider()

@st.cache_data
def load_data():
    return analise.carregar_dados()

try:
    df = load_data()
except FileNotFoundError:
    st.error("Dados não encontrados. Execute 'python gerador_dados.py' primeiro para gerar a base de dados.")
    st.stop()

# Cálculos Globais
receita_total = df['receita'].sum()
lucro_total = df['lucro'].sum()
margem_media = (lucro_total / receita_total) * 100 if receita_total > 0 else 0

# 1. Visão Geral (Cards)
st.subheader("Visão Geral Financeira", divider="gray")
col1, col2, col3 = st.columns(3)
with col1:
    render_metric_card("Receita Total", f"R$ {receita_total:,.2f}", "#10b981") # Verde
with col2:
    render_metric_card("Lucro Total", f"R$ {lucro_total:,.2f}", "#3b82f6") # Azul
with col3:
    render_metric_card("Margem Média", f"{margem_media:.2f}%", "#f59e0b") # Âmbar


st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Análise Estratégica", divider="gray")

# Layout Dinâmico
row1_col1, row1_col2 = st.columns([1.5, 1])

with row1_col1:
    # 2. Evolução Temporal (Problema de lucratividade)
    st.markdown("#### Evolução Mensal: Volume vs Lucratividade")
    st.markdown("<span style='color: var(--text-color); opacity: 0.8;'>Aumento de volume de vendas contrastando com **queda de lucro**.</span>", unsafe_allow_html=True)

    evolucao_mes = df.groupby('mes_ano').agg({'quantidade': 'sum', 'lucro': 'sum', 'receita': 'sum'}).reset_index()
    evolucao_mes = evolucao_mes.sort_values('mes_ano')

    fig_evolucao = go.Figure()
    # Barras de volume
    fig_evolucao.add_trace(go.Bar(
        x=evolucao_mes['mes_ano'], 
        y=evolucao_mes['quantidade'], 
        name='Volume (Qtd)', 
        yaxis='y1', 
        marker_color='rgba(156, 163, 175, 0.5)', # Cinza neutro
    ))
    # Linha de lucro
    fig_evolucao.add_trace(go.Scatter(
        x=evolucao_mes['mes_ano'], 
        y=evolucao_mes['lucro'], 
        name='Lucro (R$)', 
        mode='lines+markers', 
        line=dict(color='#ef4444', width=4), # Vermelho alerta
        marker=dict(size=8),
        yaxis='y2'
    ))

    fig_evolucao.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis=dict(title='Volume de Vendas', showgrid=False),
        yaxis2=dict(title='Lucro (R$)', overlaying='y', side='right', showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)

    lucro_m1 = evolucao_mes['lucro'].iloc[0]
    lucro_m6 = evolucao_mes['lucro'].iloc[-1]
    queda_perc = ((lucro_m1 - lucro_m6) / lucro_m1) * 100
    st.warning(f"**Atenção Estratégica**: O lucro caiu **{queda_perc:.1f}%** desde {evolucao_mes['mes_ano'].iloc[0]} até {evolucao_mes['mes_ano'].iloc[-1]}, apesar do aumento contínuo no volume de vendas.")

with row1_col2:
    # 3. Análise por Canal
    st.markdown("#### Receita por Canal")
    st.markdown("<span style='color: var(--text-color); opacity: 0.8;'>O canal Online domina as vendas, mas tem altos custos.</span>", unsafe_allow_html=True)
    canal_resumo = df.groupby('canal').agg({'receita': 'sum', 'lucro': 'sum'}).reset_index()
    
    fig_canal = px.pie(
        canal_resumo, 
        values='receita', 
        names='canal', 
        hole=0.5, 
        color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
    )
    fig_canal.update_layout(
        margin=dict(l=0, r=0, t=30, b=0), 
        height=320,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_canal, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Linha 2 de Layout
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    # 4. Produtos
    st.markdown("#### Margem de Lucro por Produto")
    prod_resumo = df.groupby('nome_produto').agg({'quantidade': 'sum', 'lucro': 'sum', 'receita': 'sum'}).reset_index()
    prod_resumo['margem'] = (prod_resumo['lucro'] / prod_resumo['receita']) * 100
    prod_resumo = prod_resumo.sort_values('margem', ascending=True)

    fig_prod = px.bar(
        prod_resumo, 
        x='margem', 
        y='nome_produto', 
        orientation='h', 
        text_auto='.1f', 
        color='margem', 
        color_continuous_scale='RdYlGn'
    )
    fig_prod.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Margem (%)', showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(title='', showgrid=False)
    )
    st.plotly_chart(fig_prod, use_container_width=True)
    
    prod_mais_vendido = prod_resumo.loc[prod_resumo['quantidade'].idxmax()]
    prod_mais_lucrativo = prod_resumo.loc[prod_resumo['lucro'].idxmax()]
    
    st.info(f"**Mais Vendido:** {prod_mais_vendido['nome_produto']} ({prod_mais_vendido['quantidade']} unid.)")
    st.success(f"**Mais Lucrativo:** {prod_mais_lucrativo['nome_produto']} (R$ {prod_mais_lucrativo['lucro']:,.2f})")

with row2_col2:
    # 5. Clientes (Pareto)
    st.markdown("#### Concentração de Lucro (Curva de Pareto)")
    
    clientes_lucro = df.groupby('id_cliente')['lucro'].sum().sort_values(ascending=False).reset_index()
    total_clientes = len(clientes_lucro)
    clientes_lucro['cumulativo_perc'] = (clientes_lucro['lucro'].cumsum() / lucro_total) * 100
    clientes_lucro['cliente_perc'] = (pd.Series(range(1, total_clientes + 1)) / total_clientes) * 100
    
    fig_pareto = px.line(
        clientes_lucro, x='cliente_perc', y='cumulativo_perc', 
        labels={'cliente_perc': '% de Clientes', 'cumulativo_perc': '% Acumulado do Lucro'}
    )
    fig_pareto.add_vline(x=20, line_dash="dash", line_color="#ef4444", annotation_text="20% dos Clientes")
    fig_pareto.add_hline(y=70, line_dash="dash", line_color="#ef4444", annotation_text="70% do Lucro")
    fig_pareto.update_traces(line_color='#3b82f6', line_width=3)
    fig_pareto.update_layout(
        margin=dict(l=0, r=0, t=20, b=0), 
        height=350, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

st.markdown("<div style='text-align: center; color: var(--faded-text-60); margin-top: 50px; font-size: 0.8rem;'>Desenvolvido para minicurso de Sistemas de Informação (UNEX - VCA) - SAD.</div>", unsafe_allow_html=True)