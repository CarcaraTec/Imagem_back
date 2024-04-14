from app.repository.dadosCollection_repository import DadosCollectionRepository
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

class GraficoService:

    def __init__(self):
        self.repository = DadosCollectionRepository()


    def traduzir_data_para_mes(self, data_str):
        data_obj = datetime.strptime(data_str, '%m/%d/%Y')

        nome_mes = data_obj.strftime('%B') 

        return nome_mes
    
    def gerar_grafico_sentimentos(self):
        filtro = {}
        dados = self.repository.select_random(filtro, 100)

        sentiment_data = {
            'Negative': [],
            'Positive': [],
            'Neutral': []
        }

        for dado in dados:
            sentiment = dado.get('sentiment')
            if sentiment in sentiment_data:
                data_str = dado.get('Review_Date')
                
                if data_str:
                    nome_mes = self.traduzir_data_para_mes(data_str)
                    
                    sentiment_data[sentiment].append(nome_mes)

        return sentiment_data
        

    
