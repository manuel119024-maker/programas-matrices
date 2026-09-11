import time

# Pedir tamaño de las matrices
n = int(input("Ingresa el tamaño n de las matrices: "))

# Crear matrices vacías
A = []
B = []

print("\nIngresa los valores de la matriz A:")
for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"A[{i+1}][{j+1}]: "))
        fila.append(valor)
    A.append(fila)

print("\nIngresa los valores de la matriz B:")
for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"B[{i+1}][{j+1}]: "))
        fila.append(valor)
    B.append(fila)

# Crear matriz resultado llena de ceros
C = [[0 for j in range(n)] for i in range(n)]

# Iniciar timer
inicio = time.perf_counter()

# Multiplicación de matrices
for i in range(n):
    for j in range(n):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

# Detener timer
fin = time.perf_counter()

tiempo = fin - inicio

# Mostrar matrices
print("\nMatriz A:")
for fila in A:
    print(fila)

print("\nMatriz B:")
for fila in B:
    print(fila)

print("\nResultado A x B:")
for fila in C:
    print(fila)

# Mostrar tiempo
print(f"\nTiempo de multiplicación: {tiempo:.9f} segundos")