from data import gerar,resumir,responder
def test_dataset():assert len(gerar(25))==25
def test_metrics():assert (resumir(gerar())['conversao_pct']>=0).all()
def test_question():assert 'Campanha' in responder('melhor conversão?',gerar())
