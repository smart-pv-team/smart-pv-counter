import datetime as dt

import numpy as np
from scipy import integrate


class Simpson:
    @staticmethod
    def prepare_data(data: dict):
        data_list = sorted(
            list(map(lambda x: (dt.datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S.%f%z'), x[1]), list(data.items()))),
            key=lambda x: x[0])
        data_x = [x.timestamp() for x, _ in data_list]
        data_y = [float(y) for _, y in data_list]
        min_el = 0 if not data else data_x[0]
        data_x = [round(x - min_el, 2) for x in data_x]
        return data_x, data_y

    @staticmethod
    def simpson(x: np.array, y: np.array):
        if not x.any():
            return 0
        return integrate.simpson(y, x)

    def count(self, data: dict):
        data_x, data_y = self.prepare_data(data)
        return round(self.simpson(np.array(data_x), np.array(data_y)) / 3600, 2)
