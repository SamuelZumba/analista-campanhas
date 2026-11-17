# Partner Insights — analista de campanhas

Dashboard completo com **Python, pandas, FastAPI, HTML, CSS, JavaScript e gráficos SVG**. Dados sintéticos, sem conexão com o iFood.

## Recursos funcionando
- Geração determinística de 360 registros demonstrativos e indicadores de receita, vendas, cliques, CTR, conversão e ticket médio.
- Filtros de campanha, parceiro fictício e período, aplicados em todas as métricas.
- Gráficos SVG gerados com JavaScript, tabela consolidada, exportação de CSV e perguntas em linguagem natural com interpretação **por regras em pandas**.
- Mantido `dashboard.py` antigo em Streamlit como alternativa opcional; a interface principal usa FastAPI.

## Executar
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8003
```
Abra `http://127.0.0.1:8003`. Testes: `.\.venv\Scripts\python.exe -m pytest -q`.

## Definições de métricas
- Conversão = vendas / cliques; CTR = cliques / impressões.
- Ticket médio = receita / vendas. Receita é calculada em dataset sintético, não representa vendas reais.

## Arquitetura
`data.py` gera dados → `app.py` consolida com pandas → endpoints JSON → HTML/JS renderizam tabelas e gráficos responsivos.

## Limitações
Perguntas por regras **não são uma integração de modelo LLM**. Não existe previsão de vendas, dados pessoais ou conexões com ferramentas de BI comerciais.

## Próximos passos
Pipeline de entrada de CSV validado e anonimizado, comparação de janelas de tempo, estimativas com intervalos de confiança e CI.
