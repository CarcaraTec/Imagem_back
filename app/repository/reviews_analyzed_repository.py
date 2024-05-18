from bson.objectid import ObjectId
from typing import Dict, List
from flask import current_app
from datetime import datetime
import calendar

class ReviewsAnalyzedRepository:    
    def __init__(self) -> None:
        self.__collection_name = "reviews_analyzed"

    def get_collection(self):
        db_handler = current_app.config['db_handler']
        return db_handler.get_db_connection()[self.__collection_name]

    def build_filtro_regex_tags(self, regex: str) -> dict:
        return {"Tags": {"$regex": regex, "$options": "i"}}

    def build_filtro_cidade(self, cidade: str) -> dict:
        return {"Hotel_Address": {"$regex": cidade, "$options": "i"}} if cidade else {}
    
    def build_filtro_data(self, data_inicio: str = None, data_fim: str = None) -> dict:
        if not data_inicio or not data_fim:
            return {}

        inicio_datetime = datetime.strptime(data_inicio, "%m/%Y")
        fim_datetime = datetime.strptime(data_fim, "%m/%Y")

        fim_do_mes = calendar.monthrange(fim_datetime.year, fim_datetime.month)[1]
        fim_datetime = fim_datetime.replace(day=fim_do_mes)

        return {
            "Review_Date": {
                "$gte": inicio_datetime,
                "$lte": fim_datetime
            }
        }
    
    def select_many(self, filter) -> List[Dict]:
        collection = self.get_collection()

        data = collection.find(filter)
        response = [{**elem, '_id': str(elem['_id'])} for elem in data]
        return response
    
    def select_random(self, filter, num_samples: int) -> List[Dict]:
        collection = self.get_collection()

        pipeline = [
            {"$match": filter},
            {"$sample": {"size": num_samples}}
        ]

        random_documents = collection.aggregate(pipeline)
        response = [{**elem, '_id': str(elem['_id'])} for elem in random_documents]
        return response

    def select_first(self, filter,num_samples: int) -> List[Dict]:
        collection = self.get_collection()
        data = collection.find(filter).limit(num_samples)
        response = [{**elem, '_id': str(elem['_id'])} for elem in data]
        return response

    def get_sentiment_counts(self, filtro_cidade, filtro_data) -> Dict[str, int]:
        collection = self.get_collection()

        filtro_completo = {**filtro_cidade, **filtro_data}

        pipeline = [
            {"$match": filtro_completo},
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
        ]

        print(pipeline)
        result = collection.aggregate(pipeline)
        
        sentiment_counts = {entry['_id']: entry['count'] for entry in result}
        return sentiment_counts
    
    def get_top_5_hotels_mais_bem_avaliados(self, filtro_cidade, filtro_data):
        collection = self.get_collection()

        filtro_completo = {**filtro_cidade, **filtro_data}

        pipeline =[
            {"$match": filtro_completo},
            {"$group": {"_id": "$Hotel_Name", "average_score": {"$avg": "$Reviewer_Score"}, "total_reviews": {"$sum": 1}}},
            {"$sort": {"average_score": -1, "Hotel_Name": -1, "total_reviews": -1}},
            {"$limit": 5}
        ]

        result = list(collection.aggregate(pipeline))
        return result

    def get_top_5_hotels_mais_mal_avaliados(self, filtro_cidade, filtro_data):
        collection = self.get_collection()

        filtro_completo = {**filtro_cidade, **filtro_data}

        pipeline =[
            {"$match": filtro_completo},
            {"$group": {"_id": "$Hotel_Name", "average_score": {"$avg": "$Reviewer_Score"}, "total_reviews": {"$sum": 1}}},
            {"$sort": {"average_score": 1, "Hotel_Name": 1, "total_reviews": 1}},
            {"$limit": 5}
        ]

        print(pipeline)
        result = list(collection.aggregate(pipeline))
        return result
    
    def count_documents(self, filtro) -> Dict:
        collection = self.get_collection()
        return collection.count_documents(filtro)
    
    def contagem_sentimentos_para_tipo_viagem(self, filtro_cidade, filtro_data, filtro_tipo_viagem):
        collection = self.get_collection()
  
        filtro_completo = {**filtro_cidade, **filtro_data, **filtro_tipo_viagem}

        pipeline = [
            {"$match": filtro_completo},
            {"$group": {
                "_id": "$sentiment",
                "count": {"$sum": 1}
            }}
        ]
        print(pipeline)
        resultado = collection.aggregate(pipeline)
        return resultado

    

