from flask import Flask, jsonify
from flask import request
from app.simpson import Simpson
from app.average import Average

app = Flask(__name__)
Simpson = Simpson()
Average = Average()


@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to counter app"


@app.route('/simpson', methods=['POST'])
def count_integral():
    result = Simpson.count(request.json)
    return jsonify(result)


@app.route('/average', methods=['POST'])
def count_average():
    result = Average.count(request.json)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
