import json
import matplotlib as mpl
import numpy as np

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
            category, analysis = analyze.analyze_sentiment(note)

            category_color = "green"
            if category == 'NEGATIVE':
                category_color = "background-color:red"

            sentence, word_colors = array_auseinanderfriemeln(analysis)
            flash("Completed analysis", category='success')
            return render_template("sentiment.html", category=category, category_color=category_color,
                                   zip=zip(sentence, word_colors))
    return render_template("sentiment.html")


@views.route('/irony', methods=['GET', 'POST'])
def irony():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            analyze.analyze_irony(note)
            flash("Completed analysis", category='success')

    return render_template("irony.html")


def array_auseinanderfriemeln(analysis):
    sentence = []
    word_colors = []
    analysis_sliced = analysis[1:len(analysis) - 1]
    for part in analysis_sliced:
        value = map_to_rgb(part[1])
        print(part)
        sentence.append(part[0])
        word_colors.append(f"rgb({value}, 255, {value});")
    print(word_colors)
    return sentence, word_colors


def map_to_rgb(value):
    return int(value * 255)
