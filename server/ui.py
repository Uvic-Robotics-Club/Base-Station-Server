from flask import Blueprint, request, Response, render_template

bp = Blueprint('ui', __name__, url_prefix='/ui')

@bp.route('/', methods=['GET'])
def index():
    '''
    The home page of the application which is the main dashboard 
    of the base station.
    '''

    return render_template('index.html')