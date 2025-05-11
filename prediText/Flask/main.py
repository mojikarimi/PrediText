from copy import copy
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import translators as ts
from Flask.db import get_db
import difflib
import torch
from sapling import SaplingClient
from .secure_keys import sap_api_key

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    result = None
    return render_template('main/index.html', result=result)


def grammar_check(text, lang):
    client = SaplingClient(api_key=sap_api_key)
    print(client,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    edits = client.edits(f'{text}', lang=lang, session_id="test_session")
    print(edits,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')

    gt = copy(text)
    if not edits['edits']:
        return text + 'ok shod'
    for i in edits["edits"]:
        gt = gt.replace(gt[int(i['start']):int(i['end'])], i['replacement'])
    grammar_text = gt
    return grammar_text


@bp.route('/translate', methods=('POST', 'GET'))
def translate():
    if request.method == 'POST':
        text = request.form['text']
        translate_language = request.form['translate_language']
        orig_language = request.form['orig_language']
        if orig_language in ['de', 'es', 'fr', 'sv']:
            c = [text]
            while True:
                grammar_text = grammar_check(c[-1], orig_language)
                if grammar_text.endswith('ok shod'):
                    break
                c.append(grammar_text)
            grammar_text = c[-1]
        if orig_language == 'en':
            grammar_text = happy_tt.generate_text(f"grammar: {text}", args=args).text
        if orig_language == 'ru':
            translate_text = ts.translate_text(text, from_language=orig_language, to_language=translate_language)
            grammar_text = ts.translate_text(translate_text, from_language=translate_language,
                                             to_language=orig_language)
        else:
            translate_text = ts.translate_text(grammar_text, from_language=orig_language,
                                               to_language=translate_language)

        result = {'text': text,
                  'translate_language': translate_language,
                  'translate_text': translate_text,
                  'orig_language': orig_language,
                  'grammar_text': grammar_text}
        return render_template('main/index.html', result=result)
    return redirect(url_for('index'))



def predi_word(sent, n, toker, model):
    if sent.endswith(' '):
        sent = sent.strip()
    inpts = toker(sent, return_tensors="pt")
    with torch.no_grad():
        logits = torch.argsort(model(**inpts).logits[0, -1, :], descending=True)[:n]
    sort_logits = torch.sort(logits)
    pred_words = [toker.decode([idx]).strip() for idx in sort_logits.values]
    return pred_words


@bp.route('/suggestion', methods=["POST"])
def suggestion():
    if request.method == 'POST':
        text = request.form.get('text')
        orig_lang = request.form.get('orig_lang')
        data = None
        try:
            words = text.split()
            word = words[-1]
            lang = {
                'en': english_words,
                'ru': russian_words,
                'sv': swedish_words,
                'es': spanish_words,
                'fr': french_words,
                'de': german_words,
            }
            sug_word = [i for i in difflib.get_close_matches(word, lang[orig_lang], 1000) if i.startswith(word)]
            if len(sug_word) > 10:
                sug_word = sug_word[:10]
            data = sug_word
        except IndexError:
            print('word is empty!')
        return jsonify(result=data)



@bp.route('/next_word', methods=['POST'])
def next_word():
    if request.method == 'POST':
        text = request.form.get('text')
        orig_lang = request.form.get('orig_lang')
        db = get_db()
        data = None
        split_text = text.split()
        if len(split_text) > 1:
            last_word = db.execute(
                "SELECT * FROM words WHERE org_word=? AND lang=?"
                , (split_text[-1], orig_lang,)
            ).fetchone()
            perv_word = db.execute(
                "SELECT * FROM words WHERE org_word=? AND lang=?"
                , (split_text[-2], orig_lang,)
            ).fetchone()
            if bool(last_word) is False:
                db.execute(
                    "INSERT INTO words(org_word,lang) VALUES (?,?)", (split_text[-1], orig_lang,)
                )
                db.commit()
                if perv_word is not None:  # yadet bashe perv word bar aval ke zadi None bood
                    if split_text[-1] not in eval(perv_word['next_words']):
                        my_next_word = eval(perv_word['next_words'])
                        my_next_word.append(split_text[-1])
                        db.execute(
                            "UPDATE words SET next_words=? WHERE words.id=?",
                            (str(my_next_word), perv_word['id'],)
                        )
                        db.commit()
                else:
                    db.execute(
                        "INSERT INTO words(org_word,next_words,lang) VALUES (?,?,?)",
                        (split_text[-2], str([split_text[-1]]), orig_lang,)
                    )
                    db.commit()
            else:
                data = eval(last_word['next_words'])
        else:
            my_word = db.execute(
                "SELECT * FROM words WHERE org_word=? AND lang=?"
                , (split_text[-1], orig_lang,)
            ).fetchone()
            if my_word is not None:
                data = eval(my_word['next_words'])
            else:
                db.execute(
                    "INSERT INTO words(org_word,lang) VALUES (?,?)", (split_text[-1], orig_lang,)
                )
                db.commit()
        if data is None:
            data = []
        tok_mod = {
            'en': (en_token, en_model),
            'ru': (ru_token, ru_model),
            'sv': (sv_token, sv_model),
            'es': (es_token, es_model),
            'fr': (fr_token, fr_model),
            'de': (de_token, de_model),
        }
        if len(data) < 5:
            data = predi_word(text, 10 - len(data), *tok_mod[orig_lang]) + data  # data is a list
        else:
            data = predi_word(text, 5, *tok_mod[orig_lang]) + data  # data is a list
        return jsonify(result=data)
