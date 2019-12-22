from flask import Flask, render_template

from views.music import music

app = Flask(__name__)

app.register_blueprint(music)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # debug mode - not for production
    app.run(host='0.0.0.0', debug=True, port=5000)
