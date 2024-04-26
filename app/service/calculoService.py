from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository

class CalculoService:

    def __init__(self):
        self.repository = ReviewsAnalyzedRepository()

    def gerar_calculos_cards(self):
        return self.repository.count_sentiments()
