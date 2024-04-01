from flask import Flask, request, jsonify
from app.mongoConfig.connection_options.connection import DBconnectionHandler
from app.repository.dadosCollection_repository import DadosCollectionRepository

app = Flask(__name__)
db_handle = DBconnectionHandler()
db_handle.connect_to_db()
db_connection = db_handle.get_db_connection()

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

if __name__ == '__main__':
    app.run(debug=True)