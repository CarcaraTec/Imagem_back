from app.repository.dadosCollection_repository import DadosCollectionRepository
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

class GraficoService:

    def __init__(self):
        self.repository = DadosCollectionRepository()

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
                sentiment_data[sentiment].append(dado)

        return sentiment_data