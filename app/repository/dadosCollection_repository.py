from bson.objectid import ObjectId
from typing import Dict, List
from flask import current_app

class DadosCollectionRepository:    
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
