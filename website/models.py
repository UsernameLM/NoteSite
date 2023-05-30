from . import db #from the package import the db object
from flask_login import UserMixin #ajuda a logar usuario
from sqlalchemy import func
#basicamente uma blueprint, fazer um modelo
class Note(db.Model): #um para vários user-notes
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #associar as notas para cada usuario(foreign key)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #pede um usuario válido



class User(db.Model, UserMixin): #usermixin so para usuario
    #o que vai ter nesse modelo
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True) #unique fica unico
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    notes = db.relationship('Note') #Cria a relação entre usuario e note