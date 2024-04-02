from flask import request, jsonify
from app.repository.dadosCollection_repository import DadosCollectionRepository

def register_routes(app, db_connection):
    repository = DadosCollectionRepository(db_connection)

    @app.route('/insert', methods=['POST'])
    def insert_data():
        data = request.json
        result = repository.insert_document(data)
        return jsonify(result), 201

    @app.route('/select', methods=['GET'])
    def select_data():
        filter = request.args.to_dict()
        data = repository.select_many(filter)
        return jsonify(data), 200
