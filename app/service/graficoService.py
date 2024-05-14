from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository
from datetime import datetime
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class GraficoService:

    def __init__(self):
        self.repository = ReviewsAnalyzedRepository()

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
        dados = self.repository.select_first(filtro, 100)

        sentiment_data = {
            'Negative': [],
            'Positive': [],
            'Neutral': []
        }

        for sentiment in sentiment_data:
            ocorrencias_mensais = self.contar_ocorrencias_por_mes(dados, sentiment)
            sentiment_data[sentiment] = ocorrencias_mensais
        return sentiment_data
    

    def gerar_top_5_insights_problems(self):
        filtro = {'sentiment': 'Negative'}
        dados = self.repository.select_first(filtro, 1000)
        objects = []
        hotels = ['Hotel Arena','K K Hotel George','Apex Temple Court Hotel','The Park Grand London Paddington','The Principal London']
        palavras_comuns = self.filtrar_palavras_mais_comuns(dados)
        
        for indice, nome in enumerate(hotels):
            print(f"Nome {indice + 1}: {nome}")
        
        for indice, doc in enumerate(palavras_comuns):
            objeto = {
            "hotel": hotels[indice],
            "problem": doc[0],
            "recurrence": doc[1],
            "solution": ""}
            objects.append(objeto)

        return objects
    
    def filtrar_palavras_mais_comuns(self,dados):
        
        array_strings = []

        for documento in dados:
            texto = str(documento['Negative_Review']).lower()
            texto = self.remove_stopwords(texto)
            array_strings.extend(texto.split())

        contagem_palavras = Counter(array_strings)
        palavras_comuns = contagem_palavras.most_common(5)

        
        return palavras_comuns

    def remove_stopwords(text,self):
        stop_words = set(stopwords.words('english'))
        stop_words.add('nothing')
        stop_words.add('like')
        stop_words.add('one')
        stop_words.add('us')
        stop_words.add('rooms')
        if isinstance(self, str):
            words = self.split()
            filtered_words = [word for word in words if word.lower() not in stop_words]
            return ' '.join(filtered_words)
        else:
            return ''
        
    def gerar_topo_5_hoteis_mais_bem_avaliados(self):
        return self.repository.top_5_hoteis_mais_bem_avaliados()
    
    def gerar_topo_5_hoteis_mais_mal_avaliados(self):
        return self.repository.top_5_hoteis_mais_mal_avaliados()
    
    def tipo_viagens(self, cidade):
        return self.repository.count_tipo_viagens(cidade)
    
    def comparativo_sentimentos_tipo_viagens(self, cidade):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_leisure = self.repository.build_filtro_regex_tags('Leisure trip')
        filtro_business = self.repository.build_filtro_regex_tags('Business trip')
        filtro_outros = {"$nor": [filtro_leisure, filtro_business]}

        resultados = {
            "leisure": self._processar_sentimentos(filtro_cidade, filtro_leisure),
            "business": self._processar_sentimentos(filtro_cidade, filtro_business),
            "outros": self._processar_sentimentos(filtro_cidade, filtro_outros)
        }

        return resultados

    def _processar_sentimentos(self, filtro_cidade, filtro_tipo_viagem):
        resultado = self.repository.contagem_sentimentos_para_tipo_viagem(filtro_cidade, filtro_tipo_viagem)

        total_registros = 0
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for doc in resultado:
            total_registros += doc["count"]
            if doc["_id"] in sentiment_counts:
                sentiment_counts[doc["_id"]] = doc["count"]

        porcentagem_positivos = (sentiment_counts["Positive"] / total_registros) * 100 if total_registros > 0 else 0
        porcentagem_negativos = (sentiment_counts["Negative"] / total_registros) * 100 if total_registros > 0 else 0
        porcentagem_neutros = (sentiment_counts["Neutral"] / total_registros) * 100 if total_registros > 0 else 0

        return {
            "positivos": round(porcentagem_positivos, 2),
            "negativos": round(porcentagem_negativos, 2),
            "neutros": round(porcentagem_neutros, 2)
        }

