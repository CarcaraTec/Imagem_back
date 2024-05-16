from app.repository.reviews_analyzed_repository import ReviewsAnalyzedRepository
from typing import Dict

class CalculoService:

    def __init__(self):
        self.repository = ReviewsAnalyzedRepository()

    def count_sentiments(self) -> Dict:
        sentiment_counts = self.repository.get_sentiment_counts()
        total_documents = sum(sentiment_counts.values())
        positive_count = sentiment_counts.get('Positive', 0)
        negative_count = sentiment_counts.get('Negative', 0)
        neutral_count = sentiment_counts.get('Neutral', 0)

        return {
            'Positive': positive_count,
            'Negative': negative_count,
            'Neutral': neutral_count,
            'SatisfactionIndex': (positive_count / total_documents) * 100 if total_documents > 0 else 0
        }
