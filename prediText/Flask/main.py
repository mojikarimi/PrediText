from copy import copy
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import translators as ts
from .db import get_db
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
    edits = client.edits(f'{text}', lang=lang, session_id="test_session")
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
        if orig_language in ['de', 'es', 'fr', 'sv','en']:
            c = [text]
            while True:
                grammar_text = grammar_check(c[-1], orig_language)
                if grammar_text.endswith('ok shod'):
                    break
                c.append(grammar_text)
            grammar_text = c[-1]
        # if orig_language == 'en':
        #     grammar_text = happy_tt.generate_text(f"grammar: {text}", args=args).text
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