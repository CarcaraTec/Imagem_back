from bson.objectid import ObjectId
from typing import Dict, List
from flask import current_app

class ReviewsAnalyzedRepository:    
    def __init__(self) -> None:
        self.__collection_name = "reviews_analyzed"

    def insert_document(self, document: Dict) -> Dict:
        db_handler = current_app.config['db_handler']
        collection = db_handler.get_db_connection()[self.__collection_name]
        result = collection.insert_one(document)
        document['_id'] = str(result.inserted_id)
        return document
    
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
        
        percentages = {
            'Positive': positive_count,
            'Negative': negative_count,
            'Neutral': neutral_count,
            'SatisfactionIndex': (positive_count / total_documents) * 100 if total_documents > 0 else 0
        }
        
        return percentages
    
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

        filtro_cidade = {"Hotel_Address": {"$regex": cidade}} if cidade else {}
        filtro_leisure = {"Tags": {"$regex": 'Leisure'}}
        filtro_business = {"Tags": {"$regex": 'Business'}}

        filtro_completo_leisure = {**filtro_cidade, **filtro_leisure}
        filtro_completo_business = {**filtro_cidade, **filtro_business}
        total_registros_leisure = collection.count_documents(filtro_completo_leisure)
        total_registros_business = collection.count_documents(filtro_completo_business)
        total = collection.count_documents(filtro_cidade)

        return {"total_registros_leisure": total_registros_leisure,
                "total_registros_business": total_registros_business,
                "total": total}

       
                

            
                