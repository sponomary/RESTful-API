from flask import Blueprint
from flask import request, jsonify
from back.lib.utils import token_required
from datetime import datetime

covid = Blueprint('covid', __name__)

