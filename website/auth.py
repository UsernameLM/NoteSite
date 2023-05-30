from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db, views  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash #para converter a senha

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filtrartodo usuario com email que é = email
        if user:
            if check_password_hash(user.password,password):
                flash('Login aceito', category='success')
                login_user(user, remember=True) #para não precisar ficar logando
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta', category='erro')
        else:
            flash('Email inexistente', category='erro')
        #user.password = o da tabela
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #para só acessar se ele já estiver logado
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe', category='erro')
        elif len(email)<4:
            flash("Email deve conter pelo menos 5 digitos", category='erro')
        elif len(first_name) < 2:
            flash("Nome deve conter pelo menos 3 letras", category='erro')
        elif password1 != password2:
            flash("As senhas são diferentes, digite novamene", category='erro')
        elif len(password1)<7:
            flash("Senha deve conter pelo menos 8 digitos", category='erro')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # para não precisar ficar logando
            flash("Conta criada!", category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
