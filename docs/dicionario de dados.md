# 📖 Dicionário de Dados

## Tabela: clientes_pj

| Coluna | Tipo | Descrição | Exemplo | Fonte |
|--------|------|-----------|---------|-------|
| id_cliente | int | Identificador único do cliente | 1001 | Sistema Interno |
| estado | string | UF do cliente | SP | Cadastro |
| ramo_atuacao | string | Setor de atividade | Comércio | Cadastro |
| data_fundacao | date | Data de constituição | 2010-05-15 | Receita Federal |
| faturamento_anual | float | Receita anual em R$ | 1.250.000,00 | Declarado |
| produto_credito | int | Possui crédito (1=Sim, 0=Não) | 1 | Sistema Interno |

## Tabela: campanhas_crm

| Coluna | Tipo | Descrição | Exemplo | Fonte |
|--------|------|-----------|---------|-------|
| id_campanha | int | Identificador da campanha | 101 | CRM |
| nome_campanha | string | Nome da ação | Expansão SP | Marketing |
| canal_principal | string | Canal utilizado | WhatsApp | CRM |
| leads_convertidos | int | Clientes que contrataram | 1.234 | CRM |
| roi_percentual | float | Retorno sobre investimento | 215.5 | Calculado |