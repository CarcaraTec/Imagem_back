from app.repository.dadosCollection_repository import DadosCollectionRepository
from datetime import datetime

class GraficoService:

    def __init__(self):
        self.repository = DadosCollectionRepository()

    def contar_ocorrencias_por_mes(self, dados, sentiment):
        ocorrencias_por_mes = {month: 0 for month in range(1, 13)}

        for dado in dados:
            if dado.get('sentiment') == sentiment:
                review_date_str = dado.get('Review_Date')
                if review_date_str:
                    review_date = datetime.strptime(review_date_str, '%m/%d/%Y')
                    month = review_date.month
                    ocorrencias_por_mes[month] += 1

        ocorrencias_mensais = [ocorrencias_por_mes[month] for month in range(1, 13)]
        return ocorrencias_mensais

    def gerar_grafico_sentimentos(self):
        filtro = {}
        dados = self.repository.select_random(filtro, 100)

        sentiment_data = {
            'Negative': [],
            'Positive': [],
            'Neutral': []
        }

        for sentiment in sentiment_data:
            ocorrencias_mensais = self.contar_ocorrencias_por_mes(dados, sentiment)
            sentiment_data[sentiment] = ocorrencias_mensais

        return sentiment_data
    