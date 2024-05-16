from flask import Blueprint, request, jsonify
from app.service.calculoService import CalculoService

calculo_bp = Blueprint('calculo', __name__)
calculo_service = CalculoService()

@calculo_bp.route("/cards")
def teste():
    return calculo_service.count_sentiments()