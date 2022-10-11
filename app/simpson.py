import numpy as np
from scipy import integrate


class Simpson:
    @staticmethod
    def prepare_data(data: dict):
        data_x = [float(x) for x in data.keys()]
        data_y = [float(y) for _, y in data.items()]
        return data_x, data_y

    @staticmethod
    def simpson(x: np.array, y: np.array):
        return integrate.simpson(y, x)

    def count(self, data: dict):
        data_x, data_y = self.prepare_data(data)
        return self.simpson(np.array(data_x), np.array(data_y))
