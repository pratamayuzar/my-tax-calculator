from flask import Flask, request, jsonify
from controllers.tax import TaxController

app = Flask(__name__)
engine = TaxController()


@app.route('/')
def index():
    result = {'greet': 'Welcome Home'}
    return jsonify(result)


@app.route('/tax', methods=['GET', 'POST'])
def tax():
    if request.method == 'POST':
        data = request.json
        res = engine.insert(data)
    else:
        res = engine.fetch()

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
