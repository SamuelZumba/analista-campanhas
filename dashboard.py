import streamlit as st
from data import gerar,resumir,responder
st.set_page_config(page_title='Insights de campanhas — demo',layout='wide')
st.title('Insights de campanhas · dados sintéticos')
st.caption('Dashboard demonstrativo. Nenhum dado de operação do iFood. Perguntas respondidas por regras, não por LLM.')
df=gerar();campanhas=['Todas']+list(df.campanha.unique());escolha=st.selectbox('Campanha',campanhas)
if escolha!='Todas':df=df[df.campanha==escolha]
st.metric('Receita sintética',f'R$ {df.receita.sum():,.2f}')
st.metric('Vendas',str(df.vendas.sum()))
st.dataframe(resumir(df),hide_index=True,use_container_width=True)
st.bar_chart(df.groupby('campanha')['receita'].sum())
q=st.text_input('Pergunte: qual campanha teve melhor conversão?')
if q:st.info(responder(q,df))
st.download_button('Baixar dados fictícios',df.to_csv(index=False).encode('utf-8'),'campanhas_sinteticas.csv','text/csv')
