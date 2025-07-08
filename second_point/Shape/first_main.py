from Shape import *
from math import acos,degrees,sqrt
          
p1 = Point(0, 0)
p2 = Point(1, 0)
p3 = Point(0, 1)

l1 = Line(p1, p2)
l2 = Line(p2, p3)
l3 = Line(p3, p1)

triangulo = TriRectangle(False, l1, l3)
print(triangulo.compute_inner_angles())

#a continuacion se crea un triángulo equilatero

p_eq1 = Point(0, 0)
p_eq2 = Point(1, 0)
p_eq3 = Point(0.5, sqrt(3)/2)

l_eq1 = Line(p_eq1, p_eq2)
l_eq2 = Line(p_eq2, p_eq3)
l_eq3 = Line(p_eq3, p_eq1)

# Usar la línea base l_eq1 y el tercer punto p_eq3
triangulo_equilatero = Equilateral(False, l_eq1, p_eq3)

print(triangulo_equilatero.compute_inner_angles())

#testear el cuadrado

p_sq1 = Point(0, 0)
p_sq2 = Point(1, 0)
p_sq3 = Point(1, 1)
p_sq4 = Point(0, 1)

# Crear las líneas del cuadrado en orden
l_sq1 = Line(p_sq1, p_sq2)
l_sq2 = Line(p_sq2, p_sq3)
l_sq3 = Line(p_sq3, p_sq4)
l_sq4 = Line(p_sq4, p_sq1)

# Crear el cuadrado
cuadrado = Square(True,l_sq1, l_sq2, l_sq3, l_sq4)

# Imprimir perímetro y lados
print("Perímetro:", cuadrado.compute_perimeter())
print("Lados:", [l.length for l in cuadrado.lines]) #este testeo lo hizo copilot