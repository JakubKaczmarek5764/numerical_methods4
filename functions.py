import math

import numpy as np

import integrals


class Function:
    def calc(self, x):
        pass
    def calc_points(self, a, b, step):
        x_vals = np.arange(a, b+step, step)
        y_vals = [self.calc(x) for x in x_vals]
        return list(x_vals), y_vals
class Chebyshev(Function):
    def __init__(self, deg, function):
        self.deg = deg
        self.function = function
        self.calc_polynomials()
    def calc_polynomials(self):
        self.arr = []


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

class with_weight_function(Function):
    def __init__(self, func):
        self.func = func
    def calc(self, x):
        return self.func.calc(x) * Chebyshev_weight_function.calc(x)
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

class chebyshev_polynomial(Function):

    T = []
    coefs = []
    nodes = []
    def __init__(self, function, deg):
        self.function = function
        self.deg = deg
        self.nodes = [node for (_, node) in integrals.import_gauss_coefs_from_file('chebyshev.txt')[deg]]
        self.chebyshev_coefficients()
        self.generate()
    def generate(self):
        self.T.clear()
        if self.deg >= 0:
            self.T.append(np.array([1]))
        if self.deg >= 1:
            self.T.append(np.array([1, 0]))

        for k in range(2, self.deg + 1):
            tmp_T_1 = self.T[k - 1]
            # print(tmp_T_1)
            tmp_T_2 = np.concatenate(([0, 0], self.T[k - 2]))
            # print(tmp_T_2)
            tmp_arr = 2 * tmp_T_1
            tmp_arr = np.append(tmp_arr, [0])

            tmp_arr -= tmp_T_2
            self.T.append(tmp_arr)
        self.T = [Polynomial(list(coefs)) for coefs in self.T]

    def chebyshev_coefficients(self):
        """
        Oblicza współczynniki wielomianu Czebyszewa dla funkcji f
        przy użyciu węzłów Czebyszewa.
        """
        n = len(self.nodes)
        values = [self.function.calc(x) for x in self.nodes]
        self.coefs = []
        for i in range(n):
            licznik, mianownik = 0, 0
            stopien = n
            waga = math.pi / stopien
            for j in range(n):
                T_n_x = math.cos(i * math.acos(self.nodes[j]))
                licznik += waga * values[j] * T_n_x
                mianownik += waga * T_n_x * T_n_x
            self.coefs.append(licznik / mianownik)

        return self.coefs
    def calc(self, x):
        val = 0
        for i in range(len(self.nodes)):
            val += self.coefs[i] * self.T[i].calc(x)
        return val