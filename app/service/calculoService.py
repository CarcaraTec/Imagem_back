from app.repository.dadosCollection_repository import DadosCollectionRepository

class CalculoService:

    def __init__(self):
        self.repository = DadosCollectionRepository()

    def gerar_calculos_cards(self):
        return self.repository.count_sentiments()
