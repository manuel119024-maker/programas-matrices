import time

n = int(input("Tamaño de las matrices: "))

A = []
B = []

print("\nMatriz A:")
for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"A[{i+1}][{j+1}] = "))
        fila.append(valor)
    A.append(fila)

print("\nMatriz B:")
for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"B[{i+1}][{j+1}] = "))
        fila.append(valor)
    B.append(fila)

# Iniciar timer
inicio = time.perf_counter()

# Generalización de la suma
C = []

for i in range(n):
    fila = []
    for j in range(n):
        fila.append(A[i][j] + B[i][j])
    C.append(fila)

# Terminar timer
fin = time.perf_counter()

print("\nResultado A + B:")

for fila in C:
    print(fila)

print(f"\nTiempo de cálculo: {fin-inicio:.9f} segundos")