import functions
import integrals

function = functions.Composition([functions.Trygonometrical(1), functions.Polynomial([4, 2, 5])])

obj = integrals.newton_cotes(function)
print(obj.calc(.000001))
obj2 = integrals.Gauss(function)
print(obj2.calc_integral(100))