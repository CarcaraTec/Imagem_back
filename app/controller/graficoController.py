from flask import Blueprint, request, send_file
from app.service.graficoService import GraficoService

grafico_bp = Blueprint('grafico', __name__)
grafico_service = GraficoService()

@grafico_bp.route("/", methods=['GET'])
def gerar_grafico():
    return grafico_service.gerar_grafico_sentimentos()

@grafico_bp.route("/comentarios", methods=['GET'])
def resgatar_comentarios():
    return grafico_service.gerar_top_5_insights_problems()

@grafico_bp.route("/hoteis/bem-avaliados", methods=['GET'])
def top_hoteis_bem_avaliados():
    return grafico_service.gerar_topo_5_hoteis_mais_bem_avaliados()

@grafico_bp.route("hoteis/mal-avaliados", methods=['GET'])
def top_5_hoteis_mal_avaliados():
    return grafico_service.gerar_topo_5_hoteis_mais_mal_avaliados()

@grafico_bp.route("/tipos-viagens", methods=['GET'])
def tipo_viajantes_controller():
    cidade = request.args.get('cidade') 
    
    resultado = grafico_service.tipo_viagens(cidade)

    return resultado  

@grafico_bp.route("/comparativo-viagens", methods=['GET'])
def comparativo_viajantes_controller():
    cidade = request.args.get('cidade') 
    
    resultado = grafico_service.comparativo_sentimentos_tipo_viagens(cidade)

    return resultado  
