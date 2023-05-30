#everything user related thats not authentication
from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)

@views.route("/", methods=['GET', 'POST']) #sempre que digita isso roda isso
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Adicione algo na anotação', category='erro')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Anotação adicionada', category='success')
    return render_template("home.html", user=current_user)
