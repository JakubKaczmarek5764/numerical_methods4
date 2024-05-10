import functions
import integrals

function = functions.Composition([functions.Trygonometrical(1), functions.Polynomial([4, 2, 5])])
function = functions.Trygonometrical(1)
obj = integrals.newton_cotes(function)
print(obj.calc(.00000001))
obj2 = integrals.gauss(function)
print(obj2.calc(100))