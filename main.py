import numpy as np
import matplotlib.pyplot as plt


def chebyshev_nodes(a, b, n):
    """
    Generuje n węzłów Czebyszewa w przedziale [a, b].
    """
    k = np.arange(n)
    x_cheb = np.cos((2 * k + 1) * np.pi / (2 * n))
    return 0.5 * (b - a) * (x_cheb + 1) + a


def chebyshev_coefficients(f, nodes):
    """
    Oblicza współczynniki wielomianu Czebyszewa dla funkcji f
    przy użyciu węzłów Czebyszewa.
    """
    n = len(nodes)
    values = [f(x) for x in nodes]
    coeffs = np.zeros(n)

    for k in range(n):
        coeffs[k] = (2 / n) * np.sum(values * np.cos(k * np.arccos(nodes)))

    coeffs[0] /= 2
    print(coeffs)
    return coeffs


def horner_scheme(x, coeffs):
    """
    Oblicza wartość wielomianu za pomocą schematu Hornera.
    """
    result = coeffs[-1]
    for coeff in reversed(coeffs[:-1]):
        result = result * x + coeff
    return result


# Funkcje do aproksymacji
def linear(x):
    return x


def absolute(x):
    return np.abs(x)


def polynomial(x):
    return x ** 3 - 2 * x ** 2 + x + 1


def trigonometric(x):
    return np.sin(x)


def composite_function(x):
    return np.sin(x) + x ** 3 - 2 * x ** 2 + np.abs(x) + 1


# Wybór funkcji aproksymowanej
functions = {
    'linear': linear,
    'absolute': absolute,
    'polynomial': polynomial,
    'trigonometric': trigonometric,
    'composite': composite_function
}

print("Wybierz funkcję do aproksymacji: linear, absolute, polynomial, trigonometric, composite")
func_name = input().strip()
if func_name not in functions:
    raise ValueError("Nieznana funkcja")

f = functions[func_name]

# Wybór przedziału aproksymacji
a, b = map(float, input("Podaj przedział aproksymacji (a b): ").split())

# Wybór stopnia wielomianu aproksymacyjnego
degree = int(input("Podaj stopień wielomianu aproksymacyjnego: "))

# Generowanie węzłów Czebyszewa
nodes = chebyshev_nodes(a, b, degree + 1)

# Wyznaczenie współczynników wielomianu Czebyszewa
coeffs = chebyshev_coefficients(f, nodes)

# Wyznaczenie wartości wielomianu aproksymacyjnego
x_vals = np.linspace(a, b, 400)
y_vals = f(x_vals)
approx_vals = np.array([horner_scheme(x, coeffs) for x in x_vals])

# Rysowanie wykresu
plt.plot(x_vals, y_vals, label='Oryginalna funkcja')
plt.plot(x_vals, approx_vals, label='Wielomian aproksymacyjny', linestyle='--')
plt.scatter(nodes, f(nodes), color='red', zorder=5)
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Aproksymacja funkcji {func_name} wielomianem Czebyszewa stopnia {degree}')
plt.grid(True)
plt.show()

# Obliczenie błędu aproksymacji (np. średni błąd kwadratowy)
error = np.sqrt(np.mean((y_vals - approx_vals) ** 2))
print(f"Średni błąd kwadratowy aproksymacji: {error:.6f}")
