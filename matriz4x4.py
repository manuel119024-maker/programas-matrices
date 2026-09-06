# Resolver sistema 4x4 por Gauss-Jordan (OPLU)

# Captura de datos
print("Ingresa los valores de la matriz:")

a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))
d = float(input("d = "))
e = float(input("e = "))

f = float(input("f = "))
g = float(input("g = "))
h = float(input("h = "))
i = float(input("i = "))
j = float(input("j = "))

k = float(input("k = "))
l = float(input("l = "))
m = float(input("m = "))
n = float(input("n = "))
o = float(input("o = "))

p = float(input("p = "))
q = float(input("q = "))
r = float(input("r = "))
s = float(input("s = "))
t = float(input("t = "))

# Matriz aumentada
M = [
    [a, b, c, d, e],
    [f, g, h, i, j],
    [k, l, m, n, o],
    [p, q, r, s, t]
]

print("\nMatriz original:")

for fila in M:
    print(fila)

# Gauss-Jordan
n_filas = 4

for pivote in range(n_filas):

    # Verificar si el pivote es cero
    if M[pivote][pivote] == 0:

        for fila in range(pivote + 1, n_filas):

            if M[fila][pivote] != 0:
                M[pivote], M[fila] = M[fila], M[pivote]
                break

    # Obtener valor del pivote
    valor_pivote = M[pivote][pivote]

    if valor_pivote == 0:
        print("El sistema no tiene una solución única.")
        exit()

    # Convertir pivote en 1
    for columna in range(5):
        M[pivote][columna] = M[pivote][columna] / valor_pivote

    # Hacer ceros arriba y abajo del pivote
    for fila in range(n_filas):

        if fila != pivote:

            factor = M[fila][pivote]

            for columna in range(5):

                M[fila][columna] = (
                    M[fila][columna]
                    - factor * M[pivote][columna]
                )

    print("\nPaso", pivote + 1)

    for fila in M:
        print(["{:.3f}".format(numero) for numero in fila])


# Obtener soluciones
x = M[0][4]
y = M[1][4]
z = M[2][4]
w = M[3][4]

print("\n-------------------------")
print("SOLUCIÓN")
print("-------------------------")

print("x =", round(x, 4))
print("y =", round(y, 4))
print("z =", round(z, 4))
print("w =", round(w, 4))# Resolver sistema 4x4 por Gauss-Jordan (OPLU)

# Captura de datos
print("Ingresa los valores de la matriz:")

a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))
d = float(input("d = "))
e = float(input("e = "))

f = float(input("f = "))
g = float(input("g = "))
h = float(input("h = "))
i = float(input("i = "))
j = float(input("j = "))

k = float(input("k = "))
l = float(input("l = "))
m = float(input("m = "))
n = float(input("n = "))
o = float(input("o = "))

p = float(input("p = "))
q = float(input("q = "))
r = float(input("r = "))
s = float(input("s = "))
t = float(input("t = "))

# Matriz aumentada
M = [
    [a, b, c, d, e],
    [f, g, h, i, j],
    [k, l, m, n, o],
    [p, q, r, s, t]
]

print("\nMatriz original:")

for fila in M:
    print(fila)

# Gauss-Jordan
n_filas = 4

for pivote in range(n_filas):

    # Verificar si el pivote es cero
    if M[pivote][pivote] == 0:

        for fila in range(pivote + 1, n_filas):

            if M[fila][pivote] != 0:
                M[pivote], M[fila] = M[fila], M[pivote]
                break

    # Obtener valor del pivote
    valor_pivote = M[pivote][pivote]

    if valor_pivote == 0:
        print("El sistema no tiene una solución única.")
        exit()

    # Convertir pivote en 1
    for columna in range(5):
        M[pivote][columna] = M[pivote][columna] / valor_pivote

    # Hacer ceros arriba y abajo del pivote
    for fila in range(n_filas):

        if fila != pivote:

            factor = M[fila][pivote]

            for columna in range(5):

                M[fila][columna] = (
                    M[fila][columna]
                    - factor * M[pivote][columna]
                )

    print("\nPaso", pivote + 1)

    for fila in M:
        print(["{:.3f}".format(numero) for numero in fila])


# Obtener soluciones
x = M[0][4]
y = M[1][4]
z = M[2][4]
w = M[3][4]

print("\n-------------------------")
print("SOLUCIÓN")
print("-------------------------")

print("x =", round(x, 4))
print("y =", round(y, 4))
print("z =", round(z, 4))
print("w =", round(w, 4))