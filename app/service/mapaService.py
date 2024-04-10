from app.repository.dadosCollection_repository import DadosCollectionRepository
import folium
from folium.plugins import HeatMap

def gerar_mapa_de_calor(repository: DadosCollectionRepository, sentimento: int = None) -> str:
    m = folium.Map([47.3, 8.5], zoom_start=4)

    filter = {'latitude': {'$exists': True}, 'longitude': {'$exists': True}}

    if sentimento is not None:
        filter['sentiment'] = int(sentimento)

    data = repository.select_many(filter)
    print(filter)

    coordinates = []

    for elem in data:
        lat = elem['latitude']
        lon = elem['longitude']
        coordinates.append([lat, lon])

    print(coordinates)
    HeatMap(coordinates).add_to(m)

    return m.get_root().render()
