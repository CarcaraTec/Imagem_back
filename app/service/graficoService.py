from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository
from datetime import datetime
from collections import Counter
import nltk
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
    
    def count_companhia_viagem(self, cidade):
        filtro_cidade = self.repository.build_filtro_cidade(cidade)

        filtro_companhia_familia = self.repository.build_filtro_regex_tags('Family')
        filtro_companhia_casal = self.repository.build_filtro_regex_tags('Couple')
        filtro_companhia_sozinho = self.repository.build_filtro_regex_tags('Solo')

        count_familia = self.repository.count_documents({**filtro_cidade, **filtro_companhia_familia})
        count_sozinho = self.repository.count_documents({**filtro_cidade, **filtro_companhia_sozinho})
        count_casal = self.repository.count_documents({**filtro_cidade, **filtro_companhia_casal})

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