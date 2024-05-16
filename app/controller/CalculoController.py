from flask import Blueprint, request, jsonify
from app.service.calculoService import CalculoService

calculo_bp = Blueprint('calculo', __name__)
calculo_service = CalculoService()

@calculo_bp.route("/cards")
def teste():
    cidade = request.args.get('cidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')     
    
    return calculo_service.count_sentiments(cidade, data_inicio, data_fim)