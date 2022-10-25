import datetime

import numpy as np
from scipy import integrate
import datetime as dt


class Duration:
    @staticmethod
    def prepare_data(data: dict):
        data_list = sorted(
            list(map(lambda x: (dt.datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S.%f%z'), x[1]), list(data.items()))),
            key=lambda x: x[0])
        data_x = [x for x, _ in data_list]
        data_y = [y for _, y in data_list]
        return data_x, data_y

    @staticmethod
    def duration(x: np.array, y: np.array):
        diff_sum: datetime.timedelta = datetime.timedelta()
        for i in range(1, len(x)):
            if y[i] and y[i - 1]:
                diff_sum += x[i] - x[i - 1]
        return (diff_sum.days * 24 * 60 * 60 + diff_sum.seconds) / 3600

    def count(self, data: dict):
        data_x, data_y = self.prepare_data(data)
        return self.duration(np.array(data_x), np.array(data_y))
