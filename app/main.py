import datetime
import datetime as dt

from flask import Flask, jsonify
from flask import request

from app.average import Average
from app.database import Database
from app.drawer import Drawer
from app.duration import Duration
from app.simpson import Simpson

app = Flask(__name__)
Simpson = Simpson()
Average = Average()
Duration = Duration()
Database = Database()
Drawer = Drawer()


@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to counter app"


@app.route('/simpson', methods=['POST'])
def count_integral():
    result = Simpson.count(request.json)
    return jsonify(result)


@app.route('/duration', methods=['POST'])
def count_duration():
    result = Duration.count(request.json)
    return jsonify(result)


@app.route('/average', methods=['POST'])
def count_average():
    result = Average.count(request.json)
    return jsonify(result)


@app.route('/duration/sum', methods=['POST'])
def count_duration_sum():
    data = Database.get_all_devices_consumptions()
    result = {device: Duration.count(consumptions) for device, consumptions in data.items()}
    return jsonify(result)


@app.route('/integral/sum', methods=['POST'])
def count_integral_sum():
    data = Database.get_all_devices_measurements()
    result = {device: Simpson.count(measurements) for device, measurements in data.items()}
    return jsonify(result)


@app.route('/duration/period', methods=['POST'])
def count_duration_period():
    start_time = dt.datetime.strptime(request.json["start_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    end_time = dt.datetime.strptime(request.json["end_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    data = Database.get_period_devices_consumption(start_time, end_time)
    result = {device: Duration.count(consumptions) for device, consumptions in data.items()}
    return jsonify(result)


@app.route('/integral/period', methods=['POST'])
def count_integral_period():
    start_time = dt.datetime.strptime(request.json["start_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    end_time = dt.datetime.strptime(request.json["end_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    data = Database.get_period_devices_measurements(start_time, end_time)
    result = {device: Simpson.count(measurements) for device, measurements in data.items()}
    return jsonify(result)


@app.route('/duration/period/sum', methods=['POST'])
def count_duration_period_sum():
    start_time = dt.datetime.strptime(request.json["start_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    end_time = dt.datetime.strptime(request.json["end_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    data = Database.get_period_devices_consumption(start_time, end_time)
    result = {device: Duration.count(consumptions) for device, consumptions in data.items()}
    result_sum = sum(list(map(lambda x: x[1], result.items())))
    return jsonify(result_sum)


@app.route('/integral/period/sum', methods=['POST'])
def count_integral_period_sum():
    start_time = dt.datetime.strptime(request.json["start_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    end_time = dt.datetime.strptime(request.json["end_date"], '%Y-%m-%dT%H:%M:%S.%f%z')
    data = Database.get_period_devices_measurements(start_time, end_time)
    result = {device: Simpson.count(measurements) for device, measurements in data.items()}
    result_sum = sum(list(map(lambda x: x[1], result.items()))) / 1000
    return jsonify(result_sum)


@app.route('/draw', methods=['POST'])
def draw_interval():
    power = []
    working_hours = []
    months = [8, 9, 10, 11]
    labels = ["August", "September", "October", "November"]

    for month in months:
        start_date = datetime.datetime(year=2022, month=month, day=1)
        end_date = datetime.datetime(year=2022, month=month + 1, day=1) - datetime.timedelta(days=1)
        power_data = Database.get_period_devices_measurements(start_date, end_date)
        working_hours_data = Database.get_period_devices_consumption(start_date, end_date)
        start_date = min(list(power_data.values())[0].keys(), key=lambda x: x)
        end_date = max(list(power_data.values())[0].keys(), key=lambda x: x)
        power_result = {device: Simpson.count(measurements) for device, measurements in power_data.items()}
        working_hours_result = {device: Duration.count(consumptions) for device, consumptions in
                                working_hours_data.items()}
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        days = end_date - start_date
        power_result_avg = round(sum(power_result.values()) / days.days / 1000)
        working_hours_result_avg = round(sum(working_hours_result.values()) / days.days)
        power.append(power_result_avg)
        working_hours.append(working_hours_result_avg)

    Drawer.draw(power, working_hours, labels)
    return "1"


if __name__ == '__main__':
    app.run()
