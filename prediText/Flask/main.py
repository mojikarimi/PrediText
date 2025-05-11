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

