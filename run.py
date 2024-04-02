from flask import Flask
from app.mongoConfig.connection_options.connection import DBconnectionHandler
from app.routes.dadosCollection_controller import register_routes

app = Flask(__name__)
db_handle = DBconnectionHandler()
db_handle.connect_to_db()
db_connection = db_handle.get_db_connection()

register_routes(app, db_connection)

if __name__ == '__main__':
    app.run(debug=True)
