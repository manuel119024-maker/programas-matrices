import time
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------
# PEDIR TAMAÑO DE LAS MATRICES
# ---------------------------------------

n = int(input("Ingresa el tamaño n de las matrices: "))

A = []
B = []

# ---------------------------------------
# CAPTURA DE MATRIZ A
# ---------------------------------------

print("\nIngresa los valores de la matriz A:")

for i in range(n):
    fila = []

    for j in range(n):
        valor = float(input(f"A[{i+1}][{j+1}]: "))
        fila.append(valor)

    A.append(fila)


# ---------------------------------------
# CAPTURA DE MATRIZ B
# ---------------------------------------

print("\nIngresa los valores de la matriz B:")

for i in range(n):
    fila = []

    for j in range(n):
        valor = float(input(f"B[{i+1}][{j+1}]: "))
        fila.append(valor)

    B.append(fila)


# ---------------------------------------
# CONVERTIR A MATRICES NUMPY
# ---------------------------------------

A = np.array(A)
B = np.array(B)


# ---------------------------------------
# MOSTRAR MATRICES ORIGINALES
# ---------------------------------------

print("\nMatriz A:")
print(A)

print("\nMatriz B:")
print(B)


# ---------------------------------------
# INICIAR TIMER
# ---------------------------------------

inicio = time.perf_counter()


try:

    # ---------------------------------------
    # CALCULAR INVERSA DE B
    # ---------------------------------------

    inversa_B = np.linalg.inv(B)


    # ---------------------------------------
    # PRIMER ORDEN
    # A x B^-1
    # ---------------------------------------

    C1 = A @ inversa_B


    # ---------------------------------------
    # SEGUNDO ORDEN
    # B^-1 x A
    # ---------------------------------------

    C2 = inversa_B @ A


    # ---------------------------------------
    # DETENER TIMER
    # ---------------------------------------

    fin = time.perf_counter()

    tiempo = fin - inicio


    # ---------------------------------------
    # MOSTRAR RESULTADOS
    # ---------------------------------------

    print("\n--------------------------------")
    print("INVERSA DE B")
    print("--------------------------------")

    print(inversa_B)


    print("\n--------------------------------")
    print("PRIMER RESULTADO")
    print("C1 = A x B^-1")
    print("--------------------------------")

    print(C1)


    print("\n--------------------------------")
    print("SEGUNDO RESULTADO")
    print("C2 = B^-1 x A")
    print("--------------------------------")

    print(C2)


    print("\n--------------------------------")
    print("TIEMPO DE CALCULO")
    print("--------------------------------")

    print(f"{tiempo:.9f} segundos")


    # =======================================
    # GRAFICA 1
    # A x B^-1
    # =======================================

    plt.figure()

    plt.imshow(C1)

    plt.colorbar(label="Valor")

    # Mostrar valores dentro de las celdas
    for i in range(n):

        for j in range(n):

            plt.text(
                j,
                i,
                f"{C1[i][j]:.2f}",
                ha="center",
                va="center"
            )

    plt.title("C1 = A x B^-1")

    plt.xlabel("Columnas")
    plt.ylabel("Filas")

    plt.xticks(range(n))
    plt.yticks(range(n))


    # =======================================
    # GRAFICA 2
    # B^-1 x A
    # =======================================

    plt.figure()

    plt.imshow(C2)

    plt.colorbar(label="Valor")

    # Mostrar valores dentro de las celdas
    for i in range(n):

        for j in range(n):

            plt.text(
                j,
                i,
                f"{C2[i][j]:.2f}",
                ha="center",
                va="center"
            )

    plt.title("C2 = B^-1 x A")

    plt.xlabel("Columnas")
    plt.ylabel("Filas")

    plt.xticks(range(n))
    plt.yticks(range(n))


    # Mostrar las dos gráficas
    plt.show()


# ---------------------------------------
# ERROR SI B NO TIENE INVERSA
# ---------------------------------------

except np.linalg.LinAlgError:

    print("\n--------------------------------")
    print("NO SE PUEDE REALIZAR LA OPERACION")
    print("--------------------------------")

    print("La matriz B no tiene inversa.")
    