#estrutura do banco de dados
from src import database,login_manager, app
from datetime import datetime
from flask_login import UserMixin   #diz qual classe que gerencia estrutura de login


#função obrigatoria pra estrutura de login
@login_manager.user_loader     
def load_usuario(id_usuario):                #load_nome_da_classe
    return database.session.get(Usuario, int(id_usuario))


class Usuario(database.Model,UserMixin):
   
    id = database.Column(database.Integer, primary_key= True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False,unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy = True)      
    


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key= True)
    imagem = database.Column(database.String,default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuario.id'),nullable=False,)


