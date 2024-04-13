import folium
from folium.plugins import HeatMap
from app.repository.dadosCollection_repository import DadosCollectionRepository
import math

class CalculoService:

    def __init__(self):
        self.repository = DadosCollectionRepository()

    def gerar_calculos_cards(self):
        return self.repository.count_sentiments()
