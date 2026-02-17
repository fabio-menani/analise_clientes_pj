#1. abrir terminal Ctrl + ' (aspas simples) ou Ctrl + Shift + ' para novo terminal
#2. cd caminho/para/sua/pasta/do/projeto
#3. python -m venv venv
#4. venv\Scripts\activate
#5. instale as bibliotecas pelo terminal: pip install pandas numpy
#6. para finalizar: deactivate

#importar bibliotecas
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurar seed para reproducibilidade
np.random.seed(42)
random.seed(42)

# Gerar dados de clientes PJ
n_clientes = 1000

# Listas para categorias
estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'GO', 'PE', 'CE', 'ES']
ramos = ['Comércio Varejista', 'Comércio Atacadista', 'Serviços Financeiros', 'Tecnologia', 
         'Construção Civil', 'Agronegócio', 'Indústria Manufatureira', 'Transporte e Logística',
         'Saúde', 'Educação', 'Consultoria', 'Alimentação']

# Gerar datas de referência (últimos 3 meses)
datas_ref = [datetime(2024, 1, 1), datetime(2024, 2, 1), datetime(2024, 3, 1)]

# Função para gerar datas de fundação aleatórias
def gerar_data_fundacao():
    anos = random.choices(range(1980, 2024), weights=[1]*(2024-1980))[0]
    meses = random.randint(1, 12)
    dias = random.randint(1, 28)
    return datetime(anos, meses, dias)

# Criar dataframe
clientes_pj = pd.DataFrame({
    'id_cliente': range(1, n_clientes + 1),
    'data_referencia': np.random.choice(datas_ref, n_clientes),
    'estado': np.random.choice(estados, n_clientes, p=[0.25, 0.12, 0.10, 0.08, 0.07, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06]),
    'ramo_atuacao': np.random.choice(ramos, n_clientes),
    'data_fundacao': [gerar_data_fundacao() for _ in range(n_clientes)],
})

# Calcular idade da empresa em anos
clientes_pj['idade_empresa_anos'] = (clientes_pj['data_referencia'] - clientes_pj['data_fundacao']).dt.days / 365.25

# Gerar faturamento anual baseado no ramo e idade
def gerar_faturamento(ramo, idade):
    base = {
        'Comércio Varejista': 500000,
        'Comércio Atacadista': 2000000,
        'Serviços Financeiros': 5000000,
        'Tecnologia': 3000000,
        'Construção Civil': 4000000,
        'Agronegócio': 3500000,
        'Indústria Manufatureira': 4500000,
        'Transporte e Logística': 2500000,
        'Saúde': 2800000,
        'Educação': 1800000,
        'Consultoria': 1200000,
        'Alimentação': 1500000
    }
    
    multiplicador_idade = min(1 + (idade / 20), 2.5)  # Empresas mais velhas tendem a faturar mais
    variacao = np.random.normal(1, 0.3)  # Variação aleatória
    
    return max(50000, base.get(ramo, 1000000) * multiplicador_idade * variacao)

clientes_pj['faturamento_anual'] = clientes_pj.apply(
    lambda x: gerar_faturamento(x['ramo_atuacao'], x['idade_empresa_anos']), axis=1
)

# Gerar produtos contratados (correlacionados com faturamento)
faturamento_normalizado = (clientes_pj['faturamento_anual'] - clientes_pj['faturamento_anual'].min()) / \
                         (clientes_pj['faturamento_anual'].max() - clientes_pj['faturamento_anual'].min())

# Produto de crédito (maior probabilidade para empresas com maior faturamento)
clientes_pj['produto_credito'] = (np.random.random(n_clientes) < 0.4 + 0.3 * faturamento_normalizado).astype(int)

# Financiamento de veículo (mais comum em alguns ramos)
prob_veiculo = 0.2 + 0.1 * (clientes_pj['ramo_atuacao'].isin(['Transporte e Logística', 'Agronegócio'])).astype(int)
clientes_pj['financiamento_veiculo'] = (np.random.random(n_clientes) < prob_veiculo).astype(int)

# Consórcio
clientes_pj['consorcio'] = (np.random.random(n_clientes) < 0.15).astype(int)

# Rentabilidade
clientes_pj['rentabilidade_bruta'] = clientes_pj['faturamento_anual'] * np.random.uniform(0.05, 0.15, n_clientes)
clientes_pj['rentabilidade_liquida'] = clientes_pj['rentabilidade_bruta'] * np.random.uniform(0.6, 0.85, n_clientes)

# Arredondar valores
clientes_pj['faturamento_anual'] = clientes_pj['faturamento_anual'].round(2)
clientes_pj['rentabilidade_bruta'] = clientes_pj['rentabilidade_bruta'].round(2)
clientes_pj['rentabilidade_liquida'] = clientes_pj['rentabilidade_liquida'].round(2)

# Salvar para CSV
clientes_pj.to_csv('clientes_pj_cadastro.csv', index=False, encoding='utf-8-sig')

# Mostrar primeiros registros e estatísticas
print("=== CLIENTES PESSOA JURÍDICA ===")
print(f"Total de registros: {len(clientes_pj)}")
print("\nPrimeiros 10 registros:")
print(clientes_pj.head(10))
print("\nInformações estatísticas:")
print(clientes_pj[['faturamento_anual', 'rentabilidade_bruta', 'rentabilidade_liquida', 'idade_empresa_anos']].describe())
print("\nDistribuição por estado:")
print(clientes_pj['estado'].value_counts())
print("\nDistribuição por ramo:")
print(clientes_pj['ramo_atuacao'].value_counts())
print("\nTaxa de contratação de produtos:")
print(f"Produto de Crédito: {clientes_pj['produto_credito'].mean()*100:.1f}%")
print(f"Financiamento de Veículo: {clientes_pj['financiamento_veiculo'].mean()*100:.1f}%")
print(f"Consórcio: {clientes_pj['consorcio'].mean()*100:.1f}%")