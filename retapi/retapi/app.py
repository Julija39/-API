from flask import Flask
from flask_restful import Api
from db import db
from routes import initialize_routes

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)  
api = Api(app)    

initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
