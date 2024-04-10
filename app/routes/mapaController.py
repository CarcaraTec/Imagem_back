from flask import request, jsonify
from app.repository.dadosCollection_repository import DadosCollectionRepository
from app.service.mapaService import gerar_mapa_de_calor
from app.service.mapaService import gerar_mapa_marcador

import folium
from folium import plugins
from folium.plugins import HeatMap

def register_routes(app, db_connection):
    repository = DadosCollectionRepository(db_connection)

    @app.route("/mapa-calor")
    def mapa_de_calor():
        sentimento = request.args.get('sentiment') 
        mapa_renderizado = gerar_mapa_de_calor(repository, sentimento)
        return mapa_renderizado
    
    @app.route("/mapa-marcador")
    def mapa_com_marcador():
        mapa_renderizado = gerar_mapa_marcador(repository)
        return mapa_renderizado
    
    @app.route('/insert', methods=['POST'])
    def insert_data():
        data = request.json
        result = repository.insert_document(data)
        return jsonify(result), 201
    