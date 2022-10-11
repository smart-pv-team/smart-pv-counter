import numpy as np


class Average:
    @staticmethod
    def prepare_data(x):
        return list(zip(x, list(np.arange(1, len(x), 0.2))))

    def count(self, x):
        weights = self.prepare_data(x)
        numerator = 0
        denominator = sum(list(map(lambda x: x[1], weights)))
        for x, weight in weights:
            numerator += x * weight
        return round(numerator / denominator, 2)
