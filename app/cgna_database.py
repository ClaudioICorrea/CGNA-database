from flask import (
    Blueprint, render_template
)

bp = Blueprint('cgna_database', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('cgna_database/index.html')

@bp.route('/', methods=['POST'])
def search_genes():
    return ''