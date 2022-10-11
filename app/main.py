from flask import Flask
from flask import request
from app.simpson import Simpson

app = Flask(__name__)
Simpson = Simpson()


@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to counter app"


@app.route('/count', methods=['GET'])
def count_integral():
    result = Simpson.count(request.json)
    return str(result)


if __name__ == '__main__':
    app.run()
