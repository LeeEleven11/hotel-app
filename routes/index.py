from flask import Blueprint, render_template
from config import config

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html', title=config['app']['hotel_name'], menuTitle=config['app']['hotel_name'])