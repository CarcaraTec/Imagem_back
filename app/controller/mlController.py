from flask import Blueprint, request
import app.service.mlService as mlService

ml_bp = Blueprint('ml', __name__)

@ml_bp.route("/predict")
def predict():
    text = request.args.get('text', '')
    if text:
        predicted_sentiment = mlService.predict_text(text)
        return predicted_sentiment
    else:
        return {'sentiment': 'text not provided'}, 400

