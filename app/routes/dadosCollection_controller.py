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
    
    @app.route("/mapa-calor/geral")
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
    
    @app.route("/mapa-marcador/geral")
    def mapa_com_marcador():
        m = folium.Map([47.3, 8.5], zoom_start=4)

        filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

        data = repository.select_many(filter)

        coordinates = [{'location': [elem['latitude'], elem['longitude']], 'sentiment': elem.get('sentiment', 2)} for elem in data]

        def get_sentiment_color(sentiment):
            sentiment_colors = {1: 'DarkGreen', 0: 'DarkRed', 2: 'blue'}
            return sentiment_colors.get(sentiment, 'gray')

        for coord in coordinates:
            location = coord['location']
            sentiment = coord['sentiment']
            color = get_sentiment_color(sentiment)

            folium.CircleMarker(location=location, radius=4, color=color, fill=True, fill_color=color).add_to(m)

        html_map = m.get_root().render()
        return html_map