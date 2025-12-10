import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Custos AWS vs On-Premises",
    page_icon="📊",
    layout="wide"
)

# --- Funções de Processamento de Dados ---
def clean_currency(value):
    """Remove R$, /ano e pontos, convertendo para float."""
    if isinstance(value, str):
        value = value.replace('R$', '').replace('/ano', '').replace('.', '').strip()
        return float(value)
    return float(value)

def process_economy(value):
    """Converte a coluna de economia, tratando 'Aumento' como valor negativo."""
    if isinstance(value, str):
        value = value.replace('Economia: ', '').replace('Aumento: ', '-')
        return clean_currency(value)
    return float(value)

@st.cache_data
def load_data(path):
    """Carrega e processa os dados da planilha CSV."""
    df = pd.read_csv(path)
    # Renomeia colunas para facilitar o acesso
    df.columns = ['categoria', 'on_premises', 'aws', 'economia_impacto']
    
    # Limpa e converte os dados monetários
    df['on_premises_val'] = df['on_premises'].apply(clean_currency)
    df['aws_val'] = df['aws'].apply(clean_currency)
    df['economia_val'] = df['economia_impacto'].apply(process_economy)
    
    return df

# --- Carregamento dos Dados ---
try:
    file_path = 'awsFarmaciasReduzCustos-main/Anexos/planilha-comparativa-custos.csv'
    data = load_data(file_path)
    data_summary = data[data['categoria'] != 'Totais'].copy()
except FileNotFoundError:
    st.error(f"Arquivo não encontrado em: {file_path}. Certifique-se de que o caminho está correto.")
    st.stop()


# --- Título e Introdução ---
st.title("📊 Dashboard Executivo: Análise de Custos AWS vs. On-Premises")
st.markdown("""
Este dashboard apresenta uma análise comparativa dos custos operacionais de TI, contrastando o modelo tradicional (On-Premises) com a migração para a nuvem AWS. O objetivo é demonstrar o impacto financeiro e os benefícios da adoção da AWS, conforme detalhado no relatório de implementação.
""")


# --- Exibição dos Totais ---
st.header("Resumo Financeiro Anual")
total_on_premises = data[data['categoria'] == 'Totais']['on_premises_val'].iloc[0]
total_aws = data[data['categoria'] == 'Totais']['aws_val'].iloc[0]
total_economia = data[data['categoria'] == 'Totais']['economia_val'].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Custo On-Premises Anual", f"R$ {total_on_premises:,.2f}", delta_color="normal")
col2.metric("Custo AWS Anual", f"R$ {total_aws:,.2f}", delta=f"-R$ {total_on_premises - total_aws:,.2f}", delta_color="inverse")
col3.metric("Economia Líquida Anual", f"R$ {total_economia:,.2f}", delta="Redução de 62.35%", delta_color="off")


# --- Gráficos ---
st.header("Análise Detalhada por Categoria")

col1, col2 = st.columns(2)

with col1:
    # --- Gráfico 1: Comparativo de Custos por Categoria (Barras) ---
    st.subheader("Comparativo de Custos: On-Premises vs. AWS")
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    categories = data_summary['categoria']
    on_premises_costs = data_summary['on_premises_val']
    aws_costs = data_summary['aws_val']
    
    x = np.arange(len(categories))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, on_premises_costs, width, label='On-Premises', color='#0077b6')
    rects2 = ax1.bar(x + width/2, aws_costs, width, label='AWS', color='#2ca02c')
    
    ax1.set_ylabel('Custo Anual (R$)')
    ax1.set_title('Custo Anual por Categoria')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=45, ha="right")
    ax1.legend()
    
    # Adiciona rótulos de dados
    ax1.bar_label(rects1, padding=3, fmt='R$ {:,.0f}')
    ax1.bar_label(rects2, padding=3, fmt='R$ {:,.0f}')
    
    fig1.tight_layout()
    st.pyplot(fig1)

with col2:
    # --- Gráfico 2: Composição da Economia (Pizza) ---
    st.subheader("Composição da Economia por Categoria")

    economy_composition = data_summary[data_summary['economia_val'] > 0]
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    wedges, texts, autotexts = ax2.pie(
        economy_composition['economia_val'], 
        labels=economy_composition['categoria'], 
        autopct='%1.1f%%', 
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    ax2.axis('equal')  # Garante que o gráfico seja um círculo
    ax2.set_title("Fontes de Economia na Migração para AWS")

    # Adiciona legenda com valores
    legend_labels = [f'{l}: R$ {v:,.2f}' for l, v in zip(economy_composition['categoria'], economy_composition['economia_val'])]
    ax2.legend(wedges, legend_labels, title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    st.pyplot(fig2)


# --- Tabela de Dados Detalhada ---
st.header("Tabela de Custos Detalhada")
st.markdown("A tabela abaixo mostra os valores anuais originais e os valores processados usados nos gráficos.")
# Exibe o dataframe com as colunas originais e as tratadas
st.dataframe(data[['categoria', 'on_premises', 'aws', 'economia_impacto']])


# --- Instruções para Execução ---
st.sidebar.header("Como Executar")
st.sidebar.info(
    "1. Salve este código como `app.py` no mesmo diretório do `requirements.txt`.\n"
    "2. Certifique-se de que o caminho para o CSV está correto.\n"
    "3. Abra o terminal e instale as dependências:\n"
    "   `pip install -r requirements.txt`\n"
    "4. Execute a aplicação com o comando:\n"
    "   `streamlit run app.py`"
)

st.sidebar.header("Sobre o Projeto")
st.sidebar.markdown("""
Este dashboard foi criado como uma sugestão de melhoria para o projeto **Redução dos Custos em Farmácias com AWS** do Bootcamp Santander 2025 - Ciência de Dados com Python.
""")
