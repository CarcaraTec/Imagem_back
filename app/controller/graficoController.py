from flask import Blueprint, request, jsonify
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
    cidade = request.args.get('cidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')      

    resultado = grafico_service.gerar_top_5_hoteis_mais_bem_avaliados(cidade, data_inicio, data_fim)
    return jsonify(resultado)

@grafico_bp.route("hoteis/mal-avaliados", methods=['GET'])
def top_5_hoteis_mal_avaliados():
    cidade = request.args.get('cidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')    

    resultado = grafico_service.gerar_top_5_hoteis_mais_mal_avaliados(cidade, data_inicio, data_fim)
    return jsonify(resultado)

@grafico_bp.route("/tipos-viagens", methods=['GET'])
def tipo_viajantes():
    cidade = request.args.get('cidade')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')      

    resultado = grafico_service.count_tipo_viagens(cidade, data_inicio, data_fim)
    return jsonify(resultado) 

@grafico_bp.route("/comparativo-viagens", methods=['GET'])
def comparativo_viajantes():
    cidade = request.args.get('cidade') 
    resultado = grafico_service.comparativo_sentimentos_tipo_viagens(cidade)
    return jsonify(resultado)


@grafico_bp.route("/companhia-viagens", methods=['GET'])
def companhia_viajantes():
    cidade = request.args.get('cidade') 
    resultado = grafico_service.count_companhia_viagem(cidade)
    return jsonify(resultado)  

