from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
def test_dashboard_and_filters():
 assert client.get('/').status_code==200
 opts=client.get('/api/options').json()
 assert opts['campanhas']
 stats=client.get('/api/summary').json()
 assert stats['metrics']['receita']>0
 assert stats['metrics']['registros']==360
 selection=client.get('/api/summary',params={'campanha':opts['campanhas'][0]}).json()
 assert len(selection['campanhas'])==1
 assert client.get('/api/summary',params={'campanha':'inexistente'}).status_code==422
 assert client.get('/api/summary',params={'inicio':'2026-12-01','fim':'2026-09-01'}).status_code==422
 assert client.get('/api/export').status_code==200
 assert 'Maior receita' in client.post('/api/ask',json={'pergunta':'qual a campanha com maior receita?'}).json()['resposta']

def test_static_assets():
 assert client.get('/static/style.css').status_code==200
 assert client.get('/static/app.js').status_code==200
