from copy import copy
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import translators as ts
from .db import get_db
import difflib
import torch
from sapling import SaplingClient

bp = Blueprint('main', __name__)

