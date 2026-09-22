import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------------------------------
# PEDIR TAMAÑO DE LA MATRIZ
# ---------------------------------------

n = int(input("Ingresa el tamaño de la matriz: "))

A = []

# ---------------------------------------
# CAPTURAR MATRIZ A
# ---------------------------------------

print("\nIngresa los valores de la matriz A:")

for i in range(n):
    fila = []

    for j in range(n):
        valor = float(input(f"A[{i+1}][{j+1}]: "))
        fila.append(valor)

    A.append(fila)

# Convertir a matriz NumPy
A = np.array(A)

# ---------------------------------------
# PEDIR POTENCIA
# ---------------------------------------

potencia = int(input("\nIngresa la potencia: "))

# ---------------------------------------
# INICIAR TIMER
# ---------------------------------------

inicio = time.perf_counter()

# Elevar matriz a la potencia indicada
resultado = np.linalg.matrix_power(A, potencia)

# ---------------------------------------
# DETENER TIMER
# ---------------------------------------

fin = time.perf_counter()

tiempo = fin - inicio

# ---------------------------------------
# MOSTRAR RESULTADOS
# ---------------------------------------

print("\nMatriz original A:")
print(A)

print(f"\nResultado A^{potencia}:")
print(resultado)

print(f"\nTiempo de cálculo: {tiempo:.9f} segundos")

# ---------------------------------------
# GRAFICAR RESULTADO
# Fuera del timer
# ---------------------------------------

plt.figure()

plt.imshow(resultado)

plt.colorbar(label="Valor")

# Mostrar los valores dentro de la gráfica
for i in range(n):

    for j in range(n):

        plt.text(
            j,
            i,
            f"{resultado[i][j]:.2f}",
            ha="center",
            va="center"
        )

plt.title(f"Matriz resultado A^{potencia}")

plt.xlabel("Columnas")
plt.ylabel("Filas")

plt.xticks(range(n))
plt.yticks(range(n))

plt.show()