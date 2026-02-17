#1. abrir terminal Ctrl + ' (aspas simples) ou Ctrl + Shift + ' para novo terminal
#2. cd caminho/para/sua/pasta/do/projeto
#3. python -m venv venv
#4. venv\Scripts\activate
#5. instale as bibliotecas pelo terminal: pip install pandas numpy
#6. para finalizar: deactivate

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
# Gerar dados de campanhas de CRM
n_campanhas = 20

nomes_campanhas = [
    'Expansão Empresas SP', 'Crédito PJ Nordeste', 'Financiamento Frotas', 
    'Consórcio Agro', 'Digital Onboarding', 'Retenção Clientes Top',
    'Cross-sell Consórcio', 'Upgrade Crédito', 'Expansão Sul', 
    'Novos Negócios Tech', 'Capital de Giro', 'Investimento PJ',
    'Parceria Varejo', 'Benefícios Empresa', 'Seguros Empresariais',
    'Financiamento Equipamentos', 'Conta Digital PJ', 'Antecipação Recebíveis',
    'Expansão Centro-Oeste', 'Recuperação Inativos'
]

canais = ['E-mail', 'SMS', 'WhatsApp', 'Call Center', 'App', 'Internet Banking', 'Malote']

# Gerar dados das campanhas
campanhas = pd.DataFrame({
    'id_campanha': range(1, n_campanhas + 1),
    'nome_campanha': nomes_campanhas[:n_campanhas],
    'canal_principal': np.random.choice(canais, n_campanhas),
    'data_inicio': [datetime(2023, random.randint(1, 12), random.randint(1, 20)) for _ in range(n_campanhas)],
    'data_fim': [datetime(2023, random.randint(1, 12), random.randint(1, 20)) for _ in range(n_campanhas)]
})

# Ajustar datas para que fim seja depois de início
for i in range(len(campanhas)):
    if campanhas.loc[i, 'data_fim'] < campanhas.loc[i, 'data_inicio']:
        campanhas.loc[i, 'data_fim'] = campanhas.loc[i, 'data_inicio'] + timedelta(days=random.randint(15, 45))

# Gerar métricas das campanhas
def gerar_metricas_campanha(canal):
    # Taxas de conversão por canal
    taxas_conversao = {
        'E-mail': (0.05, 0.15),
        'SMS': (0.03, 0.10),
        'WhatsApp': (0.10, 0.25),
        'Call Center': (0.08, 0.20),
        'App': (0.12, 0.30),
        'Internet Banking': (0.15, 0.35),
        'Malote': (0.01, 0.05)
    }
    
    leads = random.randint(1000, 50000)
    taxa_impacto = random.uniform(0.6, 0.95)
    leads_impactados = int(leads * taxa_impacto)
    
    min_conv, max_conv = taxas_conversao.get(canal, (0.05, 0.15))
    leads_convertidos = int(leads_impactados * random.uniform(min_conv, max_conv))
    
    return leads, leads_impactados, leads_convertidos

# Aplicar métricas
metricas = [gerar_metricas_campanha(canal) for canal in campanhas['canal_principal']]
campanhas['quantidade_leads'] = [m[0] for m in metricas]
campanhas['leads_impactados'] = [m[1] for m in metricas]
campanhas['leads_convertidos'] = [m[2] for m in metricas]

# Calcular taxas
campanhas['taxa_impacto'] = (campanhas['leads_impactados'] / campanhas['quantidade_leads'] * 100).round(2)
campanhas['taxa_conversao'] = (campanhas['leads_convertidos'] / campanhas['leads_impactados'] * 100).round(2)

# Gerar custos (baseado no canal e quantidade de leads)
custos_base = {
    'E-mail': 0.50,
    'SMS': 0.30,
    'WhatsApp': 0.40,
    'Call Center': 5.00,
    'App': 0.20,
    'Internet Banking': 0.15,
    'Malote': 10.00
}

campanhas['custo_por_lead'] = campanhas['canal_principal'].map(lambda x: custos_base.get(x, 1.00))
campanhas['custo_total'] = (campanhas['quantidade_leads'] * campanhas['custo_por_lead'] * random.uniform(0.8, 1.2)).round(2)

# Calcular receita estimada (valor médio por conversão: R$ 5.000 a R$ 50.000)
valor_medio_conversao = random.uniform(5000, 50000)
campanhas['receita_estimada'] = (campanhas['leads_convertidos'] * valor_medio_conversao).round(2)
campanhas['roi_percentual'] = ((campanhas['receita_estimada'] - campanhas['custo_total']) / campanhas['custo_total'] * 100).round(2)

# Salvar para CSV
campanhas.to_csv('campanhas_crm.csv', index=False, encoding='utf-8-sig')

print("\n\n=== CAMPANHAS DE CRM ===")
print(f"Total de campanhas: {len(campanhas)}")
print("\nPrimeiras 5 campanhas:")
print(campanhas[['nome_campanha', 'canal_principal', 'quantidade_leads', 'leads_convertidos', 
                 'taxa_conversao', 'custo_total', 'receita_estimada', 'roi_percentual']].head())
print("\nResumo por canal:")
resumo_canal = campanhas.groupby('canal_principal').agg({
    'quantidade_leads': 'sum',
    'leads_convertidos': 'sum',
    'custo_total': 'sum',
    'receita_estimada': 'sum'
}).round(2)
resumo_canal['taxa_conversao_media'] = (resumo_canal['leads_convertidos'] / resumo_canal['quantidade_leads'] * 100).round(2)
resumo_canal['roi_medio'] = ((resumo_canal['receita_estimada'] - resumo_canal['custo_total']) / resumo_canal['custo_total'] * 100).round(2)
print(resumo_canal)

print("\nTop 5 campanhas por ROI:")
print(campanhas.nlargest(5, 'roi_percentual')[['nome_campanha', 'canal_principal', 'roi_percentual', 'taxa_conversao']])