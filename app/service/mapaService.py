from app.repository.dadosCollection_repository import DadosCollectionRepository
import folium
from folium.plugins import HeatMap

def gerar_mapa_de_calor(repository: DadosCollectionRepository, sentimento: int = None) -> str:
    m = folium.Map([47.3, 8.5], zoom_start=4)

    filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

    if sentimento is not None:
        filter['sentiment'] = int(sentimento)

    data = repository.select_many(filter)

    coordinates = []

    for elem in data:
        lat = elem['latitude']
        lon = elem['longitude']
        coordinates.append([lat, lon])

    HeatMap(coordinates).add_to(m)

    return m.get_root().render()

def gerar_mapa_marcador(repository: DadosCollectionRepository):
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

    return m.get_root().render()
