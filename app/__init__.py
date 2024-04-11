from flask import Flask
from app.controller.mapaController import mapa_bp
from app.mongoConfig.connection_options.connection import DBconnectionHandler

app = Flask(__name__)

db_handler = DBconnectionHandler()
db_handler.connect_to_db()

app.register_blueprint(mapa_bp, url_prefix='/mapa')

app.config['db_handler'] = db_handler