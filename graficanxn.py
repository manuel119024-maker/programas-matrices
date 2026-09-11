import time
import matplotlib.pyplot as plt

# Pedir tamaño de las matrices
n = int(input("Ingresa el tamaño n de las matrices: "))

# Crear matrices
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

# Crear matriz resultado
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

# Mostrar resultado
print("\nMatriz A:")
for fila in A:
    print(fila)

print("\nMatriz B:")
for fila in B:
    print(fila)

print("\nMatriz resultado C = A x B:")
for fila in C:
    print(fila)

print(f"\nTiempo de multiplicación: {tiempo:.9f} segundos")

# -------------------------------
# GRAFICAR MATRIZ RESULTADO
# -------------------------------

plt.imshow(C)
plt.colorbar(label="Valor")

# Mostrar valores dentro de cada celda
for i in range(n):
    for j in range(n):
        plt.text(j, i, f"{C[i][j]:.1f}",
                 ha="center", va="center")

plt.title("Matriz resultado C = A x B")
plt.xlabel("Columnas")
plt.ylabel("Filas")

plt.xticks(range(n))
plt.yticks(range(n))

plt.show()