import folium
from folium.plugins import HeatMap
from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository
import math

class MapaService:

    def __init__(self):
        self.repository = ReviewsAnalyzedRepository()

    def gerar_mapa_de_calor(self, sentimento= None, cidade=None, data_inicio=None, data_fim=None) -> str:
        m = folium.Map([47.3, 8.5], zoom_start=5)
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)

        filter = {'lat': {'$exists': True}, 'lng': {'$exists': True}}

        if sentimento is not None:
            filter['sentiment'] = sentimento

        filter.update(filtro_cidade)
        filter.update(filtro_data)

        data = self.repository.select_random(filter, 500)

        coordinates = [
            [elem.get('lat'), elem.get('lng')] 
            for elem in data 
            if not math.isnan(elem.get('lat')) and not math.isnan(elem.get('lng'))
        ]

        HeatMap(coordinates).add_to(m)

        return m.get_root().render()

    def gerar_mapa_marcador(self, cidade=None, data_inicio=None, data_fim=None):
        m = folium.Map([47.3, 8.5], zoom_start=5)
        filtro_cidade = self.repository.build_filtro_cidade(cidade)
        filtro_data = self.repository.build_filtro_data(data_inicio, data_fim)

        filter = {'lat': {'$exists': True}, 'lng': {'$exists': True}}

        filter.update(filtro_cidade)
        filter.update(filtro_data)

        data = self.repository.select_random(filter, 100)

        coordinates = [
            {
                'location': [elem.get('lat'), elem.get('lng')],'sentiment': elem.get('sentiment')
            }
            for elem in data 
            if not math.isnan(elem.get('lat')) and not math.isnan(elem.get('lng'))
        ]

        def get_sentiment_color(sentiment):
            sentiment_colors = {'Positive': 'DarkGreen', 'Negative': 'DarkRed', 'Neutral': 'blue'}
            return sentiment_colors.get(sentiment, 'gray')

        for coord in coordinates:
            location = coord['location']
            sentiment = coord['sentiment']
            color = get_sentiment_color(sentiment)

            folium.CircleMarker(location=location, radius=4, color=color, fill=True, fill_color=color).add_to(m)

        return m.get_root().render()
    
    def insert_document(self, data):
        self.repository.insert_document(data)
