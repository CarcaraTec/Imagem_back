from flask import request, jsonify, render_template_string
from app.repository.dadosCollection_repository import DadosCollectionRepository

import folium
from folium import plugins
from folium.plugins import HeatMap

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
    
    @app.route("/mapa")
    def mapaComMarcador():
        m = folium.Map([47.3, 8.5], zoom_start=5) 

        coordinates = [
            [51.5074, -0.1278],  
            [48.8566, 2.3522],    
            [52.52, 13.405],      
            [41.9028, 12.4964],   
            [55.7558, 37.6176]    
        ]


        for coord in coordinates:
            folium.Marker(location=coord).add_to(m)

        return m.get_root().render()
    
    @app.route("/mapa-calor")
    def mapaDeCalor():
        m = folium.Map([47.3, 8.5], zoom_start=5) 

        coordinates = [
            [51.5074, -0.1278],   
            [48.8566, 2.3522],    
            [52.52, 13.405],      
            [41.9028, 12.4964],   
            [55.7558, 37.6176]    
        ]

        HeatMap(coordinates).add_to(m)

        return m.get_root().render()
    
