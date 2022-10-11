from flask import Flask
from flask import request
from app.simpson import Simpson
from app.average import Average

app = Flask(__name__)
Simpson = Simpson()
Average = Average()


@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to counter app"


@app.route('/simpson', methods=['GET'])
def count_integral():
    result = Simpson.count(request.json)
    return str(result)


@app.route('/average', methods=['GET'])
def count_average():
    result = Average.count(request.json["points"])
    return str(result)


if __name__ == '__main__':
    app.run()
