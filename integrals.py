import functions

def import_gauss_coefs_from_file(filename):
    f = open(filename)
    out = dict()
    n = 0
    while n < 100:
        n = int(f.readline().split(' ')[-1]) # number of n
        out[n] = []
        for i in range(n):

            (weight, x) = f.readline().split('  ')[1:]
            out[n].append((float(weight), float(x)))
        _ = f.readline() # empty
    f.close()
    return out
class newton_cotes:
    def __init__(self, function):
        self.function = lambda x: function.calc(x) * functions.Chebyshev_weight_function.calc(x)
    def calc(self, eps):
        out = 0

        # limit to 1
        diff = float('inf')
        l, r = 0, .5
        prev_it = self.calc_segment(l, r, eps)
        out += prev_it
        cur_it = 0
        while diff >= eps:
            l, r = r, r + abs(r - l) / 2
            cur_it = self.calc_segment(l, r, eps)
            out += cur_it
            diff = abs(prev_it - cur_it)
            prev_it = cur_it


        # limit to -1
        diff = float('inf')
        l, r = -.5, 0
        prev_it = self.calc_segment(l, r, eps)
        out += prev_it
        while diff >= eps:
            l, r = l - abs(l - r) / 2, l
            cur_it = self.calc_segment(l, r, eps)
            out += cur_it
            diff = abs(prev_it - cur_it)
            prev_it = cur_it

        return out
    def calc_segment(self, a, b, eps):
        diff = float('inf')
        num_of_intervals = 1
        prev_it = self.calc_integral(a, b, num_of_intervals)
        cur_it = 0
        while diff >= eps:
            num_of_intervals *= 2
            cur_it = self.calc_integral(a, b, num_of_intervals)
            diff = abs(prev_it - cur_it)
            prev_it = cur_it
        return cur_it

    def calc_integral(self, a, b, num_of_intervals):
        val = 0
        interval_width = b - a
        step = interval_width / (num_of_intervals * 2)

        points = [a + i * step for i in range(num_of_intervals * 2 + 1)]

        first_point_val = self.function(points[0])
        for i in range(num_of_intervals):
            last_point_val = self.function(points[2 * i + 2])
            interval_val =  step * 1/3 * (first_point_val + 4 * self.function(points[2 * i + 1]) + last_point_val)
            first_point_val = last_point_val
            val += interval_val
        return val
class gauss:
    coefs = import_gauss_coefs_from_file("chebyshev.txt")
    def __init__(self, function):
        self.function = function


    def calc(self, num_of_intervals):
        val = 0
        for (weight, x) in gauss.coefs[num_of_intervals]:
            val += weight * self.function.calc(x)
        return val
