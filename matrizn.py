# Programa para resolver sistemas de ecuaciones
# de tamaño n x n mediante Gauss-Jordan

def gauss_jordan(matriz, n):

    # Recorrer cada columna
    for i in range(n):

        # Verificar si el pivote es cero
        if matriz[i][i] == 0:

            # Buscar una fila para intercambiar
            for j in range(i + 1, n):
                if matriz[j][i] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    break
            else:
                print("El sistema no tiene solución única.")
                return None

        # Obtener el pivote
        pivote = matriz[i][i]

        # Convertir el pivote en 1
        for j in range(n + 1):
            matriz[i][j] = matriz[i][j] / pivote

        # Hacer ceros arriba y abajo del pivote
        for k in range(n):

            if k != i:

                factor = matriz[k][i]

                for j in range(n + 1):
                    matriz[k][j] = (
                        matriz[k][j]
                        - factor * matriz[i][j]
                    )

        # Mostrar proceso
        print("\nPaso", i + 1)

        for fila in matriz:
            print(
                ["{:.3f}".format(numero)
                 for numero in fila]
            )

    # Obtener las soluciones
    soluciones = []

    for i in range(n):
        soluciones.append(matriz[i][n])

    return soluciones


# ===========================
# PROGRAMA PRINCIPAL
# ===========================

n = int(input("Ingrese el tamaño de la matriz n: "))

matriz = []

print("\nIntroduzca la matriz aumentada.")
print("Debe ingresar", n + 1, "números por fila.\n")

for i in range(n):

    fila = []

    print("Fila", i + 1)

    for j in range(n):

        valor = float(
            input(
                f"Coeficiente a[{i+1}][{j+1}]: "
            )
        )

        fila.append(valor)

    resultado = float(
        input(
            f"Término independiente b[{i+1}]: "
        )
    )

    fila.append(resultado)

    matriz.append(fila)


print("\nMatriz aumentada original:")

for fila in matriz:
    print(fila)


solucion = gauss_jordan(matriz, n)


if solucion is not None:

    print("\n======================")
    print("SOLUCIÓN DEL SISTEMA")
    print("======================")

    for i in range(n):

        print(
            f"x{i+1} = {solucion[i]:.4f}"
        )