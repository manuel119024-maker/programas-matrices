import time

print("Ingresa los valores de la matriz aumentada 4x5:")

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

M = [
    [a, b, c, d, e],
    [f, g, h, i, j],
    [k, l, m, n, o],
    [p, q, r, s, t]
]

print("\nMatriz original:")
for fila in M:
    print(fila)

# -------------------------------------------------
# EL TIMER INICIA SOLO AL COMENZAR LOS CÁLCULOS
# -------------------------------------------------
tiempo_inicio = time.perf_counter()

n_filas = 4
solucion_unica = True

for pivote in range(n_filas):

    # Si el pivote es cero, buscar una fila para intercambiar
    if M[pivote][pivote] == 0:
        fila_encontrada = False

        for fila in range(pivote + 1, n_filas):
            if M[fila][pivote] != 0:
                M[pivote], M[fila] = M[fila], M[pivote]
                fila_encontrada = True
                break

        if not fila_encontrada and M[pivote][pivote] == 0:
            solucion_unica = False
            break

    valor_pivote = M[pivote][pivote]

    # Convertir el pivote en 1
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

# Obtener soluciones si existen
if solucion_unica:
    x = M[0][4]
    y = M[1][4]
    z = M[2][4]
    w = M[3][4]

# -------------------------------------------------
# EL TIMER TERMINA INMEDIATAMENTE DESPUÉS DEL CÁLCULO
# -------------------------------------------------
tiempo_fin = time.perf_counter()
tiempo_calculo = tiempo_fin - tiempo_inicio

# -------------------------------------------------
# RESULTADOS: ESTA PARTE YA NO SE CUENTA EN EL TIMER
# -------------------------------------------------
if solucion_unica:

    print("\nMatriz reducida:")
    for fila in M:
        print(["{:.3f}".format(numero) for numero in fila])

    print("\n-------------------------")
    print("SOLUCIÓN")
    print("-------------------------")

    print("x =", round(x, 4))
    print("y =", round(y, 4))
    print("z =", round(z, 4))
    print("w =", round(w, 4))

else:
    print("\nEl sistema no tiene una solución única.")

print("\n-------------------------")
print("TIEMPO DE CÁLCULO")
print("-------------------------")
print(f"{tiempo_calculo:.9f} segundos")