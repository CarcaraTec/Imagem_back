from bson.objectid import ObjectId
from typing import Dict, List
from flask import current_app

class ReviewsAnalyzedRepository:    
    def __init__(self) -> None:
        self.__collection_name = "reviews_analyzed"

    def build_filtro_tipo_viagem(self, tipo_viagem: str) -> dict:
        return {"Tags": {"$regex": tipo_viagem}}

    def build_filtro_cidade(self, cidade: str) -> dict:
        return {"Hotel_Address": {"$regex": cidade}} if cidade else {}
    
    def select_many(self, filter) -> List[Dict]:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]
        data = collection.find(filter)
        response = [{**elem, '_id': str(elem['_id'])} for elem in data]
        return response
    
    def select_random(self, filter, num_samples: int) -> List[Dict]:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]   

        pipeline = [
            {"$match": filter},
            {"$sample": {"size": num_samples}}
        ]

        random_documents = collection.aggregate(pipeline)
        response = [{**elem, '_id': str(elem['_id'])} for elem in random_documents]
        return response

    def select_first(self, filter,num_samples: int) -> List[Dict]:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]
        data = collection.find(filter).limit(num_samples) 
        response = [{**elem, '_id': str(elem['_id'])} for elem in data]
        return response

    def count_sentiments(self) -> Dict:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]

        pipeline = [
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
        ]

        result = collection.aggregate(pipeline)
        sentiment_counts = {entry['_id']: entry['count'] for entry in result} 
        total_documents = sum(sentiment_counts.values())
        positive_count = sentiment_counts.get('Positive', 0)
        negative_count = sentiment_counts.get('Negative', 0)
        neutral_count = sentiment_counts.get('Neutral', 0)

        return  {
            'Positive': positive_count,
            'Negative': negative_count,
            'Neutral': neutral_count,
            'SatisfactionIndex': (positive_count / total_documents) * 100 if total_documents > 0 else 0
        }
    
    def top_5_hoteis_mais_bem_avaliados(self) -> List[Dict]:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]

        pipeline = [
            {"$group": {"_id": "$Hotel_Name", "average_score": {"$avg": "$Average_Score"}, "total_reviews": {"$sum": 1}}},
            {"$sort": {"average_score": -1, "Hotel_Name": -1, "total_reviews": -1}},
            {"$limit": 5}
        ]

        result = list(collection.aggregate(pipeline))
        top_5_hotels = [{"Hotel_Name": entry["_id"], "Average_Score": entry["average_score"], "Total_Reviews": entry["total_reviews"]} for entry in result]
        return top_5_hotels

    def top_5_hoteis_mais_mal_avaliados(self) -> List[Dict]:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]

        pipeline = [
            {"$group": {"_id": "$Hotel_Name", "average_score": {"$avg": "$Average_Score"}, "total_reviews": {"$sum": 1}}},
            {"$sort": {"average_score": 1, "Hotel_Name": 1, "total_reviews": 1}},
            {"$limit": 5}
        ]

        result = list(collection.aggregate(pipeline))
        top_5_hotels = [{"Hotel_Name": entry["_id"], "Average_Score": entry["average_score"], "Total_Reviews": entry["total_reviews"]} for entry in result]
        return top_5_hotels
    
    def count_tipo_viagens(self, cidade=None) -> Dict:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]

        filtro_cidade = self.build_filtro_cidade(cidade)
        filtro_leisure = self.build_filtro_tipo_viagem('Leisure trip')
        filtro_business = self.build_filtro_tipo_viagem('Business trip')

        filtro_completo_leisure = {**filtro_cidade, **filtro_leisure}
        filtro_completo_business = {**filtro_cidade, **filtro_business}

        total = collection.count_documents(filtro_cidade)
        leisure = collection.count_documents(filtro_completo_leisure) / total * 100 
        business = collection.count_documents(filtro_completo_business) / total * 100 
        outros = (100 - business - leisure)
        
        return {"total": total,
                "leisure": round(leisure, 2),
                "business": round(business, 2),
                "outros": round(outros, 2)}
    
    def comparativo_sentimentos_tipo_viagens(self, cidade):
        filtro_cidade = self.build_filtro_cidade(cidade)
        filtro_leisure = self.build_filtro_tipo_viagem('Leisure trip')
        filtro_business = self.build_filtro_tipo_viagem('Business trip')
        filtro_outros = {"$nor": [filtro_leisure, filtro_business]}

        resultados = {
            "leisure": self._contagem_sentimentos_para_tipo_viagem(filtro_cidade, filtro_leisure),
            "business": self._contagem_sentimentos_para_tipo_viagem(filtro_cidade, filtro_business),
            "outros": self._contagem_sentimentos_para_tipo_viagem(filtro_cidade, filtro_outros)
        }

        return resultados

    def _contagem_sentimentos_para_tipo_viagem(self, filtro_cidade, filtro_tipo_viagem):
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]

        filtro_completo = {**filtro_cidade, **filtro_tipo_viagem}

        pipeline = [
            {"$match": filtro_completo},
            {"$group": {
                "_id": "$sentiment",
                "count": {"$sum": 1}
            }}
        ]

        resultado = collection.aggregate(pipeline)

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
            