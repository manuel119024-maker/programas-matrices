import time

def gauss_jordan(matriz, n):
    for i in range(n):
        if matriz[i][i] == 0:
            for j in range(i + 1, n):
                if matriz[j][i] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    break
            else:
                return None

        pivote = matriz[i][i]

        for j in range(n + 1):
            matriz[i][j] = matriz[i][j] / pivote

        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(n + 1):
                    matriz[k][j] = matriz[k][j] - factor * matriz[i][j]

    soluciones = []
    for i in range(n):
        soluciones.append(matriz[i][n])

    return soluciones

n = int(input("Ingrese el tamaño de la matriz n: "))
matriz = []

print("\nIntroduzca la matriz aumentada.")
print("Debe ingresar", n + 1, "números por fila.\n")

for i in range(n):
    fila = []
    print("Fila", i + 1)

    for j in range(n):
        valor = float(input(f"Coeficiente a[{i+1}][{j+1}]: "))
        fila.append(valor)

    resultado = float(input(f"Término independiente b[{i+1}]: "))
    fila.append(resultado)
    matriz.append(fila)

print("\nMatriz aumentada original:")
for fila in matriz:
    print(fila)

tiempo_inicio = time.perf_counter()
solucion = gauss_jordan(matriz, n)
tiempo_fin = time.perf_counter()

if solucion is None:
    print("El sistema no tiene solución única.")
else:
    print("\n======================")
    print("SOLUCIÓN DEL SISTEMA")
    print("======================")
    for i in range(n):
        print(f"x{i+1} = {solucion[i]:.4f}")

print(f"\nTiempo de cálculo: {tiempo_fin - tiempo_inicio:.9f} segundos")