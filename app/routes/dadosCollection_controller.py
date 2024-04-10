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
        m = folium.Map([47.3, 8.5], zoom_start=4) 

        filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

        data = repository.select_many(filter)

        coordinates = []

        for elem in data:
            lat = elem['latitude']
            lon = elem['longitude']
            coordinates.append([lat, lon])

        for coord in coordinates:
            folium.CircleMarker(location=coord, radius=4, color='red', fill=True, fill_color='red').add_to(m)

        return m.get_root().render()
    
    @app.route("/mapa-calor")
    def mapaDeCalor():
        m = folium.Map([47.3, 8.5], zoom_start=4)

        filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

        data = repository.select_many(filter)

        coordinates = []

        for elem in data:
            lat = elem['latitude']
            lon = elem['longitude']
            coordinates.append([lat, lon])

        HeatMap(coordinates).add_to(m)

        return m.get_root().render()
    
    @app.route("/mapa-teste")
    def mapaComMarcador1():
        m = folium.Map([47.3, 8.5], zoom_start=4) 

        filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

        data = repository.select_many(filter)

        coordinates = []
        sentiment_colors = {1: 'DarkGreen', 0: 'DarkRed', 2: 'blue'} 

        for elem in data:
            lat = elem['latitude']
            lon = elem['longitude']
            sentiment = elem.get('sentiment', 2) 

            coordinates.append({'location': [lat, lon], 'sentiment': sentiment})

        for coord in coordinates:
            location = coord['location']
            sentiment = coord['sentiment']
            color = sentiment_colors.get(sentiment, 'gray') 

            folium.CircleMarker(location=location, radius=4, color=color, fill=True, fill_color=color).add_to(m)

        html_map = m.get_root().render()

        return html_map
        
