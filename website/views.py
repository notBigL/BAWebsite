import json
import matplotlib as mpl

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from . import analyze

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            analyze.analyze_sentiment(note)
            flash("Note added", category='success')

    return render_template("home.html")


@views.route("/delete-note", methods=["POST"])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            result = analyze.analyze_sentiment(note)
            flash("Completed analysis", category='success')
            return render_template("sentiment.html", result=result)
    return render_template("sentiment.html")


@views.route('/irony', methods=['GET', 'POST'])
def irony():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            analyze.analyze_sentiment(note)
            flash("Completed analysis", category='success')

    return render_template("irony.html")
