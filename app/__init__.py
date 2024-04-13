from flask import Flask
from flask_cors import CORS
from app.controller.mapaController import mapa_bp
from app.controller.CalculoController import calculo_bp
from app.mongoConfig.connection_options.connection import DBconnectionHandler

app = Flask(__name__)
CORS(app)

db_handler = DBconnectionHandler()
db_handler.connect_to_db()

app.register_blueprint(mapa_bp, url_prefix='/mapa')
app.register_blueprint(calculo_bp, url_prefix='/calculos')

app.config['db_handler'] = db_handler