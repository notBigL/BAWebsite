import json

from flask import Blueprint, render_template, request, flash, jsonify
from . import analyze

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@views.route('analyse/<model>', methods=['GET', 'POST'])
def analyse(model):
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 6:
            flash("Text is too short", category='error')
        else:
            category, analysis, html_thingy = analyze.analyze_sentence(note, model)

            category_color = "green"
            if category == 'NEG' or category == 'non_irony':
                category_color = "red"

            sentence, word_colors = take_array_apart(analysis, category == 'POSITIVE' or category == 'irony')
            flash("Completed analysis", category='success')
            return render_template("analyse.html", category=category, category_color=category_color,
                                   zip=zip(sentence, word_colors), model=model, note=note, html_thingy=html_thingy)
    return render_template("analyse.html", model=model)


def take_array_apart(analysis, positive):
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


@views.route('analyse-post-only', methods=['POST'])
def analyse_and_give_to_frontend():
    try:
        data = request.get_json()
        data = json.dumps(data)
        data = json.loads(data)
        category, analysis, html_thingy = analyze.analyze_sentence(data['sentence'], data['model'])

        return jsonify(html_thingy), 200
    except Exception as e:
        error_response = {'error': str(e)}
        return jsonify(error_response), 500


def map_to_rgb(value):
    if value >= 0:
        return abs(int(value * 230) - 230) - 25
    else:
        return abs(int(value * 230) + 230) - 25
