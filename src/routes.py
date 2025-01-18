#definir rotas
from flask import render_template,url_for, redirect
from src import app,database, login_manager,bcrypt
from flask_login import login_required,login_user,logout_user, current_user
from src.forms import FormCriarConta, FormLogin,FormFoto
from src.models import Usuario,Foto
import os
from werkzeug.utils import secure_filename

@app.route('/',methods=["GET","POST"])
def homepage():
    formlogin= FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil",id_usuario=usuario.id))  #redirecionar para perfil
    return render_template("homepage.html",form= formlogin)


@app.route("/criarconta",methods=["GET","POST"])
def criar_conta():
    form_criarconta= FormCriarConta()
    if form_criarconta.validate_on_submit():
        print("Formulário validado!")  #apagar depois
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)  #criptografar senha
        usuario = Usuario(username=form_criarconta.username.data , 
                          senha=senha , email=form_criarconta.email.data)
        database.session.add(usuario)   
        database.session.commit()
        login_user(usuario, remember=True)        
        return redirect(url_for("perfil",id_usuario=usuario.id))  #redirecionar para rota perfil
    return render_template("criar_conta.html",form=form_criarconta)


@app.route("/perfil/<id_usuario>",methods=["GET","POST"])         #url dinamica   
@login_required                         #tela acessivel após realizar login
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
    #o user ta vendo o perfil dele
        form_foto= FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar aquivo fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), #caminho arquivo atual 
                              app.config["UPLOAD_FOLDER"], nome_seguro)   #caminho fotos_post
            arquivo.save(caminho)
            #registrar esse arquivo no banco
            foto = Foto(imagem=nome_seguro  , id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            # Após salvar a foto, buscar as fotos do usuário para passar para o template
            usuario = Usuario.query.get(int(id_usuario))  # Recupera o usuário do banco de dados
            fotos = usuario.fotos
          
        return  render_template("perfil.html",usuario=current_user,form=form_foto)

    else:
        usuario = Usuario.query.get(int(id_usuario))

        return render_template("perfil.html",usuario=usuario,form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))



@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html",fotos=fotos)