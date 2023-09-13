import json
import matplotlib as mpl
import numpy as np

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import Note
from . import db
from . import analyze

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
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


@views.route('analyse/<model>', methods=['GET', 'POST'])
def analyse(model):
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            category, analysis = analyze.analyze_sentence(note, model)

            category_color = "green"
            if category == 'NEGATIVE' or category == 'non_irony':
                category_color = "red"

            sentence, word_colors = array_auseinanderfriemeln(analysis, category == 'POSITIVE' or category == 'irony')
            flash("Completed analysis", category='success')
            return render_template("analyse.html", category=category, category_color=category_color,
                                   zip=zip(sentence, word_colors), model=model, note=note)
    return render_template("analyse.html", model=model)


def array_auseinanderfriemeln(analysis, positive):
    sentence = []
    word_colors = []
    analysis_sliced = analysis[1:len(analysis) - 1]
    for part in analysis_sliced:
        value = map_to_rgb(part[1])
        sentence.append(part[0])
        if positive:
            if part[1] >= 0:
                word_colors.append(f"rgb({value}, 255, {value});")
            else:
                word_colors.append(f"rgb(255, {value}, {value});")
        else:
            if part[1] >= 0:
                word_colors.append(f"rgb(255, {value}, {value});")
            else:
                word_colors.append(f"rgb({value}, 255, {value});")
    print(word_colors)
    return sentence, word_colors


def map_to_rgb(value):
    if value >= 0:
        return abs(int(value * 230) - 230) - 25
    else:
        return abs(int(value * 230) + 230) - 25
