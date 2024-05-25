import random

import functions
import matplotlib.pyplot as plt

import integrals


def file_input(name):
    f = open(name, "r")
    nodes = []
    for line in f:
        nodes.append(tuple(float(x) for x in line.strip().split(',')))
    f.close()
    return nodes

def plotting(func, a=-.999, b=.999, points=None, step=None):
    if not step:
        step = abs(a - b)/100
    x_vals, y_vals = func.calc_points(a, b, step)
    plt.grid(True)
    if not points:
        plt.plot(x_vals, y_vals, label="Wykres funkcji f(x)")
    if points:
        plt.plot(x_vals, y_vals, label="Wielomian interpolacyjny")

    plt.axhline(y=0, c='green')
    if a <= 0 <= b:
        plt.axvline(x=0, c='green')
    if points:
        plt.scatter(x=[point[0] for point in points], y=[point[1] for point in points], color='C5', label="Węzeł")
        plt.legend(loc="best")
def input_polynomial():
    print("Podaj wspolczynniki wielomianu po spacji: ")
    coefs = [float(x) for x in input().split()]
    return functions.Polynomial(coefs)
def input_trygonometrical():
    print("Podaj rodzaj funkcji trygonometrycznej: ")
    print("0 - sin \n1 - cos\n2 - tan \n3 - ctg")
    index = int(input())
    return functions.Trygonometrical(index)

def intro(): # zlozenia funkcji podawane sa od lewej do prawej, czyli w przypadku zlozenia f(g(x)) najpierw podajemy funkcje f

    print("Wybierz z ilu funkcji ma byc zlozenie:")
    count = int(input())
    funcs = []
    for i in range(count):
        print(f"Wybierz rodzaj funkcji {i+1}: \n0 - Wielomianowa \n1 - Trygonometryczna \n2 - Moduł")
        choice = int(input())
        if choice == 0:
            funcs.append(input_polynomial())
        elif choice == 1:
            funcs.append(input_trygonometrical())
        elif choice == 2:
            funcs.append(functions.Abs())
        else:
            raise Exception("Zly wybor")

    output_function = functions.Composition(funcs)

    print("Wprowadz krance przedzialu po spacji: ")
    (a, b) = (float(x) for x in input().split())
    print("Wprowadz liczbe wezlow: ")
    num_of_nodes = int(input())
    print("Wprowadz sposob wprowadzania wezlow: \n0 - z pliku \n1 - jitter")
    method = int(input())
    if (method == 0):
        print("Wprowadz nazwe pliku: ")
        points = file_input(str(input()))
    if (method == 1):
        x_points = jitter(a, b, num_of_nodes)
        points = [(x, output_function.calc(x)) for x in x_points]

    print(points)
    interpolate(output_function, a, b, points)

def interpolate(func, a, b, points):
    plotting(func, a, b)
    interpolated_func = functions.interpolation_newton_polynomial(points)
    plotting(interpolated_func, a, b, points, color='C1', linestyle='solid')

def jitter(a, b, num_of_nodes, _range = None):
    step = (b - a) / (num_of_nodes - 1)
    if not _range: _range = step / 4

    x_points = [(a + i * step) for i in range(num_of_nodes)]

    return [a] + [one_point_jitter(x, _range) for x in x_points[1:-1]] + [b]

def one_point_jitter(x, range):
    return x - (random.random() * range - range / 2)



def built_in_functions():

    funcs = [
        functions.Polynomial([0.5, 1]),         # liniowa
        # functions.Polynomial([2.1, 2.3, -2.5]), # wielomian
        # functions.Trygonometrical(0),           # trygonometryczna
        # functions.Abs(),
        # functions.Composition([functions.Polynomial([-1, 0]), functions.Abs()]),

        # functions.Composition([functions.Trygonometrical(0),
        #                        functions.Polynomial([10, 0])]),
        # functions.Composition([functions.Polynomial([2.1, 2.3, -2.5]),
        #                        functions.Exponential(2.1),
        #                        functions.Trygonometrical(1)]),  # złożenie
        functions.Composition([functions.Polynomial([8, 3]),    # huhu
                               functions.Trygonometrical(0),
                               functions.Polynomial([15, 0])])

    ]

    degrees = [2, 5, 10]

    for i, func in enumerate(funcs):
        plotting(func)
        for degree in degrees:
            plotting(functions.chebyshev_polynomial(func, degree))
            print(functions.chebyshev_polynomial(func, degree).error())
        plt.show()
