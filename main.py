from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'insert datboi here'

if __name__ == '__main__':
    # debug mode - not for production
    app.run(host='0.0.0.0', debug=True, port=5000)
