from pymongo import MongoClient
from app.mongoConfig.connection_options.mongo_db_configs import config

class DBconnectionHandler:
    def __init__(self) -> None:
        self.__conexao_string = 'mongodb+srv://Carcara:{}@cct.rabwqh8.mongodb.net/?retryWrites=true&w=majority&appName=CCT'.format(
            config["password"]
        )
        self.__database_name = config["db_name"]
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__conexao_string)
        self.__db_connection = self.__client[self.__database_name]
        
    def get_db_connection(self):
        return self.__db_connection
        
    def get_db_client(self):
        return self.__client
        