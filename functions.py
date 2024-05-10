import math

import numpy as np


class Function:
    def calc(self, x):
        pass
    def calc_points(self, a, b, step):
        x_vals = np.arange(a, b+step, step)

        y_vals = [self.calc(x) for x in x_vals]
        return list(x_vals), y_vals
class Chebyshev_weight_function(Function):
    @staticmethod
    def calc(x):
        return 1 / (math.sqrt(1 - x ** 2))
class Abs(Function):
    def calc(self, x):
        return abs(x)

class Polynomial(Function):
    def __init__(self, coefs):
        if len(coefs) > 0:
            self.coefs = coefs
        else:
            raise Exception("No coefficients")

    def calc(self, x):
        result = self.coefs[0]
        for coef in self.coefs[1:]:
            result = coef + x * result
        return result


class Trygonometrical(Function):
    def __init__(self, func_index):
        if func_index == 0:
            self.func = math.sin
        elif func_index == 1:
            self.func = math.cos
        elif func_index == 2:
            self.func = math.tan
        elif func_index == 3:
            self.func = lambda x: 1 / math.tan(x)
        else:
            raise Exception("Wrong index")


    def calc(self, x):
        return self.func(x)


class Exponential(Function):
    def __init__(self, b):
        if b > 0:

            self.b = b
        else:
            raise Exception("Wrong base")
    def calc(self, x):
        return self.b ** x


class Composition(Function):
    def __init__(self, functions):
        if len(functions) > 0:
            self.functions = functions
        else:
            raise Exception("No functions")

    def calc(self, x):
        result = x
        for function in reversed(self.functions):
            result = function.calc(result)
        return result
