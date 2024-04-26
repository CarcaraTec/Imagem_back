from flask import Blueprint, request, jsonify
from app.service.mapaService import MapaService

mapa_bp = Blueprint('mapa', __name__)
mapa_service = MapaService()

@mapa_bp.route("/calor")
def mapa_de_calor():
    sentimento = request.args.get('sentiment') 
    mapa_renderizado = mapa_service.gerar_mapa_de_calor(sentimento)
    return mapa_renderizado

@mapa_bp.route("/marcador")
def mapa_com_marcador():
    mapa_renderizado = mapa_service.gerar_mapa_marcador()
    return mapa_renderizado
