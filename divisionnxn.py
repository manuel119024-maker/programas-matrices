import time
import numpy as np
import matplotlib.pyplot as plt

# Pedir tamaño de las matrices
n = int(input("Ingresa el tamaño n de las matrices: "))

A = []
B = []

# -----------------------------
# CAPTURA DE MATRIZ A
# -----------------------------

print("\nIngresa los valores de la matriz A:")

for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"A[{i+1}][{j+1}]: "))
        fila.append(valor)
    A.append(fila)

# -----------------------------
# CAPTURA DE MATRIZ B
# -----------------------------

print("\nIngresa los valores de la matriz B:")

for i in range(n):
    fila = []
    for j in range(n):
        valor = float(input(f"B[{i+1}][{j+1}]: "))
        fila.append(valor)
    B.append(fila)

# Convertir a matrices NumPy
A = np.array(A)
B = np.array(B)

# -----------------------------
# INICIAR TIMER
# -----------------------------

inicio = time.perf_counter()

try:

    # Calcular inversa de B
    inversa_B = np.linalg.inv(B)

    # División matricial
    C = A @ inversa_B

    # Detener timer
    fin = time.perf_counter()

    tiempo = fin - inicio

    # -----------------------------
    # MOSTRAR RESULTADOS
    # -----------------------------

    print("\nMatriz A:")
    print(A)

    print("\nMatriz B:")
    print(B)

    print("\nInversa de B:")
    print(inversa_B)

    print("\nResultado C = A x B^-1:")
    print(C)

    print(f"\nTiempo de cálculo: {tiempo:.9f} segundos")

    # -----------------------------
    # GRAFICAR RESULTADO
    # -----------------------------

    plt.imshow(C)

    plt.colorbar(label="Valor")

    # Mostrar valores dentro de las celdas
    for i in range(n):
        for j in range(n):

            plt.text(
                j,
                i,
                f"{C[i][j]:.2f}",
                ha="center",
                va="center"
            )

    plt.title("División de matrices C = A x B^-1")

    plt.xlabel("Columnas")
    plt.ylabel("Filas")

    plt.xticks(range(n))
    plt.yticks(range(n))

    plt.show()

except np.linalg.LinAlgError:

    print("\nNo se puede realizar la división.")
    print("La matriz B no tiene inversa.")