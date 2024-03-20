import os
from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from .app.routes import api_blueprint
from src.app.config.extensions import db, ma

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"
db.init_app(app)
ma.init_app(app)
app.register_blueprint(api_blueprint)