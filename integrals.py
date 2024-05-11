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
        num_of_nodes = 1
        # limit to 1
        diff = float('inf')
        l, r = 0, .5
        prev_it, _ = self.calc_segment(l, r, eps)
        out += prev_it
        while diff >= eps:
            l, r = r, r + abs(r - l) / 2
            cur_it, tmp_num_of_nodes = self.calc_segment(l, r, eps)
            out += cur_it
            diff = abs(prev_it - cur_it)
            prev_it = cur_it
            num_of_nodes += tmp_num_of_nodes

        # limit to -1
        diff = float('inf')
        l, r = -.5, 0
        prev_it, _ = self.calc_segment(l, r, eps)
        out += prev_it
        while diff >= eps:
            l, r = l - abs(l - r) / 2, l
            cur_it, tmp_num_of_nodes = self.calc_segment(l, r, eps)
            out += cur_it
            diff = abs(prev_it - cur_it)
            prev_it = cur_it
            num_of_nodes += tmp_num_of_nodes
        return (out, num_of_nodes)
    def calc_segment(self, a, b, eps):
        diff = float('inf')
        num_of_intervals = 1
        a_val = self.function(a)
        b_val = self.function(b)
        interval_width = b - a
        step = interval_width / (num_of_intervals * 2)
        prev_it = (step / 3) * (a_val + b_val + 4 * self.function(a + abs(b - a) / 2))
        while diff >= eps:
            num_of_intervals *= 2
            cur_it = a_val + b_val
            interval_width = b - a
            step = interval_width / (num_of_intervals * 2)
            points = [a + i * step for i in range(num_of_intervals * 2 + 1)]
            for i in range(1, num_of_intervals):
                cur_it += 4 * self.function(points[2 * i - 1])
                cur_it += 2 * self.function(points[2 * i])
            cur_it += 4 * self.function(points[-2])
            cur_it *= step / 3
            diff = abs(prev_it - cur_it)
            prev_it = cur_it
        return (cur_it, len(points) - 1)

class gauss:
    coefs = import_gauss_coefs_from_file("chebyshev.txt")
    def __init__(self, function):
        self.function = function

    def calc(self, num_of_intervals: int):
        val = 0
        for (weight, x) in gauss.coefs[num_of_intervals]:
            val += weight * self.function.calc(x)
        return val

