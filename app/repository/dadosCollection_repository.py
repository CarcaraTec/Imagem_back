from bson.objectid import ObjectId
from typing import Dict, List
from datetime import timedelta

class DadosCollectionRepository:
    def __init__(self, db_connection) -> None:
        self.__collection_name = "dadosCollection"
        self.__db_connection = db_connection

    
    def insert_document(self, document: Dict) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        result = collection.insert_one(document)
        document['_id'] = str(result.inserted_id)
        return document
    
    def select_many(self, filter) -> List[Dict]:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(filter)

        response = [{**elem, '_id': str(elem['_id'])} for elem in data]

        return response
