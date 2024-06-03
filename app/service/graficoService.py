from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository
from datetime import datetime
from collections import Counter
import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')

class GraficoService:

    def __init__(self):
        self.repository = ReviewsAnalyzedRepository()
        
    def gerar_top_5_hoteis_mais_bem_avaliados(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio,data_fim)

        result = self.repository.get_top_5_hotels_mais_bem_avaliados(filtro_cidade, filtro_data)
        top_5_hotels = [{"Hotel_Name": entry["_id"], "Average_Score": round(entry["average_score"], 2), "Total_Reviews": entry["total_reviews"]} for entry in result]
        return top_5_hotels
    
    def gerar_top_5_hoteis_mais_mal_avaliados(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio,data_fim)

        result = self.repository.get_top_5_hotels_mais_mal_avaliados(filtro_cidade, filtro_data)
        top_5_hotels = [{"Hotel_Name": entry["_id"], "Average_Score": round(entry["average_score"], 2), "Total_Reviews": entry["total_reviews"]} for entry in result]
        return top_5_hotels
    
    def count_tipo_viagens(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)
        filtro_leisure = self.repository.build_filtro_regex_tags('Leisure trip')
        filtro_business = self.repository.build_filtro_regex_tags('Business trip')

        filtro_completo_leisure = {**filtro_cidade, **filtro_data, **filtro_leisure}
        filtro_completo_business = {**filtro_cidade, **filtro_data, **filtro_business}
        filtro_completo_cidade_data = {**filtro_cidade, **filtro_data}
        
        total = self.repository.count_documents(filtro_completo_cidade_data)
        leisure = self.repository.count_documents(filtro_completo_leisure) / total * 100 if total > 0 else 0
        business = self.repository.count_documents(filtro_completo_business) / total * 100 if total > 0 else 0   
        outros = 100 - business - leisure
        
        return {
            "total": total,
            "leisure": round(leisure, 2),
            "business": round(business, 2),
            "outros": round(outros, 2)
        }

    
    def comparativo_sentimentos_tipo_viagens(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_leisure = self.repository.build_filtro_regex_tags('Leisure trip')
        filtro_business = self.repository.build_filtro_regex_tags('Business trip')
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)
        filtro_outros = {"$nor": [filtro_leisure, filtro_business]}

        resultados = {
            "leisure": self._processar_sentimentos(filtro_cidade, filtro_data, filtro_leisure),
            "business": self._processar_sentimentos(filtro_cidade, filtro_data, filtro_business),
            "outros": self._processar_sentimentos(filtro_cidade, filtro_data, filtro_outros)
        }

        return resultados

    def _processar_sentimentos(self, filtro_cidade, filtro_data, filtro_tipo_viagem):
        resultado = self.repository.contagem_sentimentos_para_tipo_viagem(filtro_cidade, filtro_data, filtro_tipo_viagem)

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
    
    def count_tempo_hospedagem_percentual(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)
        resultado = self.repository.count_tempo_hospedagem_percentual(filtro_cidade, filtro_data)
        
        

        count_2_ou_menos = 0
        count_3_a_4 = 0
        count_mais_de_4 = 0
        total_reviews = 0

        for doc in resultado:
            if doc["_id"] == "2 ou menos noites":
                count_2_ou_menos = doc["count"]
            elif doc["_id"] == "3 a 4 noites":
                count_3_a_4 = doc["count"]
            elif doc["_id"] == "mais de 4 noites":
                count_mais_de_4 = doc["count"]
            total_reviews += doc["count"]

        if total_reviews == 0:
            return {
                "2 ou menos noites": 0,
                "3 a 4 noites": 0,
                "mais de 4 noites": 0
            }

        percentual_2_ou_menos = (count_2_ou_menos / total_reviews) * 100
        percentual_3_a_4 = (count_3_a_4 / total_reviews) * 100
        percentual_mais_de_4 = (count_mais_de_4 / total_reviews) * 100

        return {
            "2 ou menos noites": round(percentual_2_ou_menos, 2),
            "3 a 4 noites": round(percentual_3_a_4, 2),
            "mais de 4 noites": round(percentual_mais_de_4, 2)
        }

    def count_companhia_viagem(self, cidade=None, data_inicio=None, data_fim=None):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)
        filtro_companhia_familia = self.repository.build_filtro_regex_tags('Family')
        filtro_companhia_casal = self.repository.build_filtro_regex_tags('Couple')
        filtro_companhia_sozinho = self.repository.build_filtro_regex_tags('Solo')

        filtro_completo_family = {**filtro_cidade, **filtro_data, **filtro_companhia_familia}
        filtro_completo_solo = {**filtro_cidade, **filtro_data, **filtro_companhia_sozinho}
        filtro_completo_casal = {**filtro_cidade, **filtro_data, **filtro_companhia_casal}

        count_familia = self.repository.count_documents(filtro_completo_family)
        count_sozinho = self.repository.count_documents(filtro_completo_solo)
        count_casal = self.repository.count_documents(filtro_completo_casal)

        total = count_familia + count_sozinho + count_casal

        return {
            "familia": round((count_familia / total) * 100, 2),
            "sozinho": round((count_sozinho / total) * 100, 2),
            "casal": round((count_casal / total) * 100, 2)
        }

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