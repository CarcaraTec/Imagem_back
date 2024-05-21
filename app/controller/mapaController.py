from flask import Blueprint, request, jsonify
from app.service.mapaService import MapaService

mapa_bp = Blueprint('mapa', __name__)
mapa_service = MapaService()

@mapa_bp.route("/calor")
def mapa_de_calor():
    sentimento = request.args.get('sentiment') 
    cidade = request.args.get('cidade') 
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    mapa_renderizado = mapa_service.gerar_mapa_de_calor(sentimento, cidade, data_inicio, data_fim)
    return mapa_renderizado

@mapa_bp.route("/marcador")
def mapa_com_marcador():
    cidade = request.args.get('cidade') 
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    mapa_renderizado = mapa_service.gerar_mapa_marcador(cidade, data_inicio, data_fim)
    return mapa_renderizado
