"""Dados sintéticos determinísticos, nunca obtidos do iFood."""
import random
from datetime import date,timedelta
from pathlib import Path
import pandas as pd

def gerar(n=180,seed=42):
    rng=random.Random(seed);records=[]
    for i in range(n):
        exibicoes=rng.randint(300,1800);cliques=rng.randint(20,max(20,exibicoes//5));vendas=rng.randint(0,min(25,cliques))
        records.append({'data':str(date(2026,9,1)+timedelta(days=i%60)),'restaurante':f'Parceiro DEMO-{i%12:02d}','campanha':['Cupom Leve','Combo Primavera','Novos Clientes'][i%3],'impressoes':exibicoes,'cliques':cliques,'vendas':vendas,'receita':round(vendas*rng.uniform(19,60),2)})
    return pd.DataFrame(records)
def resumir(df):
    x=df.groupby('campanha',as_index=False)[['cliques','impressoes','vendas','receita']].sum()
    x['conversao_pct']=(100*x['vendas']/x['cliques'].clip(lower=1)).round(2)
    return x.sort_values('conversao_pct',ascending=False)
def responder(pergunta,df):
    q=pergunta.lower()
    if 'convers' in q: return 'Campanha com melhor conversão: '+resumir(df).iloc[0]['campanha']
    if 'receita' in q or 'venda' in q:
        r=df.groupby('restaurante')['receita'].sum().sort_values(ascending=False)
        return f'Maior receita sintética: {r.index[0]} — R$ {r.iloc[0]:.2f}'
    return 'Pergunte por conversão, receita ou vendas. Interpretação local por regras, sem LLM.'
if __name__=='__main__':
    path=Path(__file__).parent/'dados_sinteticos.csv';gerar().to_csv(path,index=False);print(path)
