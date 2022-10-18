import numpy as np


class Average:
    @staticmethod
    def prepare_data(x):
        step = 0.7
        return list(zip(x, list(np.arange(1, len(x)*step, step))))

    def count(self, x):
        if len(x) == 1:
            return x[0]
        if not x:
            return 0
        weights = self.prepare_data(x)
        numerator = 0
        denominator = sum(list(map(lambda x: x[1], weights)))
        for x, weight in weights:
            numerator += x * weight
        return round(numerator / denominator, 2)
