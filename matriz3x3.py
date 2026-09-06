a = float(input("Ingresa a: "))
b = float(input("Ingresa b: "))
c = float(input("Ingresa c: "))
d = float(input("Ingresa d: "))

e = float(input("Ingresa e: "))
f = float(input("Ingresa f: "))
g = float(input("Ingresa g: "))
h = float(input("Ingresa h: "))

i = float(input("Ingresa i: "))
j = float(input("Ingresa j: "))
k = float(input("Ingresa k: "))
l = float(input("Ingresa l: "))

# Determinante
det = a*f*k - a*g*j - b*e*k + b*g*i + c*e*j - c*f*i

if det == 0:
    print("El sistema no tiene una solución única.")
else:
    # Calcular x
    x = (d*f*k - d*g*j - b*h*k + b*g*l + c*h*j - c*f*l) / det

    # Calcular y
    y = (a*h*k - a*g*l - d*e*k + d*g*i + c*e*l - c*h*i) / det

    # Calcular z
    z = (a*f*l - a*h*j - b*e*l + b*h*i + d*e*j - d*f*i) / det

    print("\nResultados:")
    print("x =", x)
    print("y =", y)
    print("z =", z)