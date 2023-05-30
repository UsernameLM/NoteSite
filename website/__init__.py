from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db= SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lapluma'     #cookie chave

    # Salvar na pasta do programa
    current_directory = os.path.dirname(os.path.abspath(__file__))
    #para anterior usar current_directory = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    DB_PATH = os.path.join(current_directory, DB_NAME)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}' #para salvar na pasta website

    db.init_app(app) #abrir database

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note #importar as coisas do models.py, pode colocar só import .models tbm
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # onde ir caso nao logado
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id): #falando com user pela primary key
        return User.query.get(int(id))

    return app

