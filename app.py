"""Partner Insights: dashboard Python/FastAPI sobre dataset inteiramente sintético."""
import io
from datetime import date
from pathlib import Path
from fastapi import FastAPI,Query,HTTPException
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
import pandas as pd
from data import gerar,resumir,responder
BASE=Path(__file__).resolve().parent
app=FastAPI(title='Partner Insights | dados sintéticos',version='2.0')
app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
DATA=gerar(360,seed=42)
class Filters(BaseModel):
 campanha:str|None=None
 restaurante:str|None=None
 inicio:date|None=None
 fim:date|None=None
class Question(BaseModel):
 pergunta:str=Field(min_length=3,max_length=300)
 campanha:str|None=None
 restaurante:str|None=None
 inicio:date|None=None
 fim:date|None=None

def filtered(q:Filters):
 df=DATA.copy()
 if q.inicio and q.fim and q.inicio>q.fim:raise HTTPException(422,'A data inicial é maior que a final.')
 if q.campanha:
  if q.campanha not in DATA['campanha'].unique():raise HTTPException(422,'Campanha inexistente')
  df=df[df.campanha==q.campanha]
 if q.restaurante:
  if q.restaurante not in DATA['restaurante'].unique():raise HTTPException(422,'Restaurante inexistente')
  df=df[df.restaurante==q.restaurante]
 if q.inicio:df=df[df.data>=q.inicio.isoformat()]
 if q.fim:df=df[df.data<=q.fim.isoformat()]
 return df

def metrics(df):
 clicks=int(df.cliques.sum());views=int(df.impressoes.sum());sales=int(df.vendas.sum());revenue=round(float(df.receita.sum()),2)
 return {'receita':revenue,'vendas':sales,'cliques':clicks,'impressoes':views,
 'conversao_pct':round(100*sales/clicks,2) if clicks else 0,
 'ctr_pct':round(100*clicks/views,2) if views else 0,
 'ticket_medio':round(revenue/sales,2) if sales else 0,
 'registros':int(len(df))}

def aggregate(df,col):
 if df.empty:return []
 x=df.groupby(col,as_index=False)[['receita','vendas','cliques','impressoes']].sum()
 x['conversao_pct']=(100*x.vendas/x.cliques.clip(lower=1)).round(2)
 x=x.sort_values('receita',ascending=False)
 return x.to_dict('records')

def answer(q:str,df):
 if df.empty:return 'Nenhum registro encontrado para esses filtros. Ajuste o período ou a seleção.'
 question=q.lower()
 by=aggregate(df,'campanha')
 if 'convers' in question:
  best=max(by,key=lambda x:x['conversao_pct'])
  return f"Maior conversão do recorte: {best['campanha']} ({best['conversao_pct']:.2f}% de vendas por clique). Esta é uma análise determinística, não gerada por LLM."
 if 'campanha' in question and ('receita' in question or 'venda' in question or 'melhor' in question):
  best=max(by,key=lambda x:x['receita'])
  return f"Maior receita no recorte: {best['campanha']}, R$ {best['receita']:.2f}."
 if 'restaurante' in question or 'parceiro' in question:
  best=max(aggregate(df,'restaurante'),key=lambda x:x['receita'])
  return f"Parceiro com maior receita no recorte: {best['restaurante']} (R$ {best['receita']:.2f})."
 if 'ticket' in question:
  return f"Ticket médio sintético por venda: R$ {metrics(df)['ticket_medio']:.2f}."
 if 'ctr' in question or 'clique' in question:
  return f"CTR do recorte: {metrics(df)['ctr_pct']:.2f}% (cliques / impressões)."
 return 'Pergunte sobre melhor campanha, conversão, receita, parceiro, cliques, CTR ou ticket médio. Respostas locais baseadas em pandas.'

@app.middleware('http')
async def headers(request,call_next):
 r=await call_next(request)
 r.headers['X-Content-Type-Options']='nosniff';r.headers['X-Frame-Options']='DENY'
 r.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
 return r
@app.get('/')
def homepage():return FileResponse(BASE/'templates'/'index.html')
@app.get('/health')
def health():return {'ok':True,'data':'sinteticos','records':len(DATA)}
@app.get('/api/options')
def options():return {'campanhas':sorted(DATA.campanha.unique().tolist()),'restaurantes':sorted(DATA.restaurante.unique().tolist()),'inicio':str(DATA.data.min()),'fim':str(DATA.data.max())}
@app.get('/api/summary')
def summary(campanha:str|None=None,restaurante:str|None=None,inicio:date|None=None,fim:date|None=None):
 df=filtered(Filters(campanha=campanha,restaurante=restaurante,inicio=inicio,fim=fim))
 daily=aggregate(df,'data')
 return {'metrics':metrics(df),'campanhas':aggregate(df,'campanha'),'parceiros':aggregate(df,'restaurante'),
 'diario':sorted(daily,key=lambda x:x['data']),'data':'sinteticos','fonte':'Faker-like / Python random seed 42'}
@app.post('/api/ask')
def ask(q:Question):
 df=filtered(Filters(campanha=q.campanha,restaurante=q.restaurante,inicio=q.inicio,fim=q.fim))
 return {'resposta':answer(q.pergunta,df),'modo':'analise-regras-pandas','registros':len(df)}
@app.get('/api/export')
def export(campanha:str|None=None,restaurante:str|None=None,inicio:date|None=None,fim:date|None=None):
 df=filtered(Filters(campanha=campanha,restaurante=restaurante,inicio=inicio,fim=fim))
 data=df.to_csv(index=False,sep=';').encode('utf-8-sig')
 return StreamingResponse(io.BytesIO(data),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':'attachment; filename="dados_campanhas_sinteticos.csv"'})
