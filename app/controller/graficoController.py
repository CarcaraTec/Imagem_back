from flask import Blueprint, request, send_file
from app.service.graficoService import GraficoService

grafico_bp = Blueprint('grafico', __name__)
grafico_service = GraficoService()

@grafico_bp.route("/", methods=['GET'])
def gerar_grafico():
    return grafico_service.gerar_grafico_sentimentos()

@grafico_bp.route("/comentarios", methods=['GET'])
def resgatar_comentarios():
    return grafico_service.gerar_top_5_insights()