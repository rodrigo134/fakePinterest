from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt  import Bcrypt


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

app.config["SECRET_KEY"] = "e17131e7c28e1c0f70a5607a854091ec"  #chave de segurança do app
app.config["UPLOAD_FOLDER"]= "static/fotos_posts"
database = SQLAlchemy(app)
bcrypt = Bcrypt(app) #criptografar senha
login_manager = LoginManager(app)
login_manager.login_view = "homepage"   #route que gerencia login

import src.models
# Apenas importe a função após a criação do app
'''Ao importar models.py no arquivo __init__.py, 
o decorador @login_manager.user_loader já registra a função load_usuario no login_manager
'''

from src import routes