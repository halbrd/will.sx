from flask import Blueprint, render_template

music = Blueprint('music', __name__)

@music.route('/music/')
def index():
    return render_template('music/index.html')
