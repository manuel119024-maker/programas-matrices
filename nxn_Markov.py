# ============================================================
# EJERCICIO 1
# ANÁLISIS TEMPORAL DE UN GRAFO ALEATORIO NxN
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time


# ============================================================
# 1. PEDIR TAMAÑO DE LA MATRIZ
# ============================================================

n = int(
    input("\nIngresa el tamaño n de la matriz NxN: ")
)

if n < 2:
    print("\nERROR: El tamaño debe ser mínimo 2.")
    exit()


# ============================================================
# 2. CREAR NOMBRES DE LOS NODOS
# ============================================================

nodos = []

for i in range(n):
    nodos.append(f"N{i+1}")


# ============================================================
# 3. GENERAR MATRIZ ALEATORIA DE CONEXIONES
# ============================================================
#
# 0 = No existe conexión
# 1 = Existe conexión
#
# FILA    = nodo de origen
# COLUMNA = nodo de destino
#
# ============================================================

A = np.random.randint(
    0,
    2,
    size=(n, n)
)


# ============================================================
# 4. ELIMINAR AUTOCONEXIONES
# ============================================================
#
# La diagonal principal será igual a cero.
#
# ============================================================

np.fill_diagonal(A, 0)


# ============================================================
# 5. GARANTIZAR AL MENOS UNA SALIDA POR NODO
# ============================================================
#
# Evitamos que algún nodo quede completamente aislado
# en sus conexiones de salida.
#
# ============================================================

for i in range(n):

    if np.sum(A[i, :]) == 0:

        posibles_destinos = []

        for j in range(n):

            if j != i:
                posibles_destinos.append(j)

        destino = np.random.choice(
            posibles_destinos
        )

        A[i, destino] = 1


# ============================================================
# 6. IMPRIMIR MATRIZ ORIGINAL DE CONEXIONES
# ============================================================

print("\n")
print("=" * 60)
print("           MATRIZ ORIGINAL DE CONEXIONES")
print("=" * 60)

print(A)


# ============================================================
# 7. MOSTRAR LAS CONEXIONES GENERADAS
# ============================================================

print("\n")
print("=" * 60)
print("              CONEXIONES DEL GRAFO")
print("=" * 60)


for i in range(n):

    for j in range(n):

        if A[i, j] == 1:

            print(
                f"{nodos[i]}  --->  {nodos[j]}"
            )


# ============================================================
# 8. CREAR MATRIZ DE TRANSICIÓN M
# ============================================================
#
# Si un nodo tiene k conexiones de salida,
# su probabilidad se divide entre ellas:
#
# peso = 1/k
#
# Para poder realizar:
#
# T(k+1) = M * T(k)
#
# colocamos el peso como:
#
# M[destino, origen]
#
# ============================================================

M = np.zeros(
    (n, n),
    dtype=float
)


for origen in range(n):

    destinos = []

    for destino in range(n):

        if A[origen, destino] == 1:

            destinos.append(destino)


    cantidad_salidas = len(destinos)


    if cantidad_salidas > 0:

        peso = 1 / cantidad_salidas


        for destino in destinos:

            M[destino, origen] = peso


# ============================================================
# 9. CONFIGURAR IMPRESIÓN DE MATRICES
# ============================================================

np.set_printoptions(
    precision=4,
    suppress=True
)


# ============================================================
# 10. IMPRIMIR MATRIZ DE TRANSICIÓN
# ============================================================

print("\n")
print("=" * 60)
print("              MATRIZ DE TRANSICIÓN M")
print("=" * 60)

print(M)


# ============================================================
# 11. COMPROBAR LA MATRIZ
# ============================================================
#
# Cada columna debe sumar aproximadamente 1.
#
# ============================================================

print("\nSuma de cada columna:")

print(
    np.sum(
        M,
        axis=0
    )
)


# ============================================================
# 12. VECTOR INICIAL T0
# ============================================================
#
# Todos los nodos comienzan con la misma popularidad:
#
# 1/n
#
# ============================================================

T0 = np.ones(
    (n, 1),
    dtype=float
) / n


T = T0.copy()


print("\n")
print("=" * 60)
print("                  VECTOR INICIAL T0")
print("=" * 60)

print(T0)


# ============================================================
# 13. MOSTRAR POPULARIDAD INICIAL
# ============================================================

print("\nPOPULARIDAD INICIAL:")


for i in range(n):

    print(
        f"{nodos[i]} = "
        f"{T0[i,0] * 100:.4f}%"
    )


print(
    f"\nSuma total = "
    f"{np.sum(T0) * 100:.4f}%"
)


# ============================================================
# 14. PEDIR NÚMERO DE ITERACIONES
# ============================================================

iteraciones = int(
    input(
        "\n¿Cuántas iteraciones deseas realizar? "
    )
)


if iteraciones < 1:

    print(
        "\nERROR: El número de iteraciones "
        "debe ser mayor que cero."
    )

    exit()


# ============================================================
# 15. CREAR HISTORIAL
# ============================================================

historial = [
    T.flatten().copy()
]


# ============================================================
# 16. INICIAR TIMER
# ============================================================

inicio = time.perf_counter()


# ============================================================
# 17. REALIZAR ITERACIONES
# ============================================================
#
# T1 = M * T0
# T2 = M * T1
# T3 = M * T2
#
# ...
#
# Tk = M^k * T0
#
# ============================================================

for k in range(
    1,
    iteraciones + 1
):

    # Multiplicación matricial

    T = M @ T


    # Guardar resultado

    historial.append(
        T.flatten().copy()
    )


    # --------------------------------------------------------
    # IMPRIMIR RESULTADO DE LA ITERACIÓN
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)

    print(
        f"                    ITERACIÓN T{k}"
    )

    print("=" * 60)


    print("\nVector resultante:")

    print(T)


    print("\nPopularidades:")


    for i in range(n):

        print(
            f"{nodos[i]} = "
            f"{T[i,0] * 100:.4f}%"
        )


    print(
        f"\nSuma = "
        f"{np.sum(T) * 100:.4f}%"
    )


# ============================================================
# 18. DETENER TIMER
# ============================================================

fin = time.perf_counter()


tiempo = (
    fin - inicio
)


# ============================================================
# 19. CALCULAR NUEVA MATRIZ M^k
# ============================================================
#
# Esta es la parte que faltaba.
#
# Si se solicitaron 5 iteraciones:
#
# M_nueva = M^5
#
# ============================================================

M_nueva = np.linalg.matrix_power(
    M,
    iteraciones
)


# ============================================================
# 20. IMPRIMIR NUEVA MATRIZ
# ============================================================

print("\n")
print("=" * 60)

print(
    f"              NUEVA MATRIZ M^{iteraciones}"
)

print("=" * 60)

print(M_nueva)


# ============================================================
# 21. COMPROBAR RESULTADO USANDO M^k
# ============================================================
#
# Debemos obtener:
#
# Tk = M^k * T0
#
# ============================================================

T_comprobacion = (
    M_nueva @ T0
)


print("\n")
print("=" * 60)
print("             COMPROBACIÓN MATEMÁTICA")
print("=" * 60)


print(
    f"\nT{iteraciones} = "
    f"M^{iteraciones} * T0"
)


print("\nResultado:")

print(
    T_comprobacion
)


# ============================================================
# 22. RESULTADO FINAL
# ============================================================

print("\n")
print("=" * 60)
print("                  RESULTADO FINAL")
print("=" * 60)


for i in range(n):

    print(
        f"{nodos[i]} = "
        f"{T[i,0] * 100:.4f}%"
    )


# ============================================================
# 23. IDENTIFICAR NODO MÁS POPULAR
# ============================================================

indice_mayor = np.argmax(
    T[:,0]
)


print("\n")
print("=" * 60)
print("                 NODO MÁS POPULAR")
print("=" * 60)


print(
    f"\nNodo: "
    f"{nodos[indice_mayor]}"
)


print(
    f"Popularidad: "
    f"{T[indice_mayor,0] * 100:.4f}%"
)


# ============================================================
# 24. MOSTRAR TIMER
# ============================================================

print(
    f"\nTiempo total de cálculo = "
    f"{tiempo:.9f} segundos"
)


# ============================================================
# 25. CONVERTIR HISTORIAL A ARRAY
# ============================================================

historial = np.array(
    historial
)


# ============================================================
# 26. TABLA COMPLETA DE ITERACIONES
# ============================================================

print("\n")
print("=" * 60)
print("                TABLA DE ITERACIONES")
print("=" * 60)


print("\nIteración", end="")


for nodo in nodos:

    print(
        f"\t{nodo}",
        end=""
    )


print()


for k in range(
    iteraciones + 1
):

    print(
        f"T{k}",
        end=""
    )


    for i in range(n):

        print(
            f"\t{historial[k,i] * 100:.2f}%",
            end=""
        )


    print()


# ============================================================
# 27. GRÁFICA DE EVOLUCIÓN TEMPORAL
# ============================================================

plt.figure(
    figsize=(11, 7)
)


for i in range(n):

    plt.plot(
        range(iteraciones + 1),
        historial[:,i] * 100,
        marker="o",
        label=nodos[i]
    )


plt.xlabel(
    "Iteración"
)


plt.ylabel(
    "Popularidad (%)"
)


plt.title(
    "Evolución temporal de los nodos"
)


plt.xticks(
    range(iteraciones + 1)
)


plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)


plt.grid()


plt.tight_layout()


plt.show()


# ============================================================
# 28. CREAR GRAFO DIRIGIDO
# ============================================================

G = nx.DiGraph()


G.add_nodes_from(
    nodos
)


# ============================================================
# 29. AGREGAR CONEXIONES AL GRAFO
# ============================================================

for i in range(n):

    for j in range(n):

        if A[i,j] == 1:

            G.add_edge(
                nodos[i],
                nodos[j]
            )


# ============================================================
# 30. CREAR POSICIONES AUTOMÁTICAS
# ============================================================

pos = nx.spring_layout(
    G,
    seed=42
)


# ============================================================
# 31. GRAFICAR GRAFO
# ============================================================

plt.figure(
    figsize=(12, 8)
)


# ------------------------------------------------------------
# NODOS
# ------------------------------------------------------------

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=2200
)


# ------------------------------------------------------------
# CONEXIONES CON FLECHAS
# ------------------------------------------------------------

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=25,
    width=1.8,
    connectionstyle="arc3,rad=0.08",
    min_source_margin=20,
    min_target_margin=20
)


# ============================================================
# 32. CREAR ETIQUETAS CON POPULARIDAD FINAL
# ============================================================

etiquetas = {}


for i in range(n):

    etiquetas[nodos[i]] = (
        f"{nodos[i]}\n"
        f"{T[i,0] * 100:.2f}%"
    )


# ------------------------------------------------------------
# ETIQUETAS
# ------------------------------------------------------------

nx.draw_networkx_labels(
    G,
    pos,
    labels=etiquetas,
    font_size=9,
    font_weight="bold"
)


plt.title(
    f"Grafo temporal aleatorio {n} x {n}\n"
    "Las flechas indican la dirección de las conexiones"
)


plt.axis("off")


plt.tight_layout()


plt.show()


# ============================================================
# 33. GRAFICAR NUEVA MATRIZ M^k
# ============================================================

plt.figure(
    figsize=(8, 7)
)


plt.imshow(
    M_nueva,
    aspect="auto"
)


plt.colorbar(
    label="Valor"
)


plt.xlabel(
    "Nodo de origen"
)


plt.ylabel(
    "Nodo de destino"
)


plt.title(
    f"Nueva matriz M^{iteraciones}"
)


plt.xticks(
    range(n),
    nodos,
    rotation=45
)


plt.yticks(
    range(n),
    nodos
)


# ============================================================
# 34. MOSTRAR VALORES SOBRE LA MATRIZ
# ============================================================

for i in range(n):

    for j in range(n):

        plt.text(
            j,
            i,
            f"{M_nueva[i,j]:.2f}",
            ha="center",
            va="center"
        )


plt.tight_layout()


plt.show()


# ============================================================
# 35. RESUMEN FINAL
# ============================================================

print("\n")
print("=" * 60)
print("                    RESUMEN")
print("=" * 60)


print(
    f"\nTamaño de la matriz = "
    f"{n} x {n}"
)


print(
    f"Número de iteraciones = "
    f"{iteraciones}"
)


print(
    f"Número de conexiones = "
    f"{int(np.sum(A))}"
)


print(
    f"Nodo más popular = "
    f"{nodos[indice_mayor]}"
)


print(
    f"Popularidad final = "
    f"{T[indice_mayor,0] * 100:.4f}%"
)


print(
    f"Tiempo de cálculo = "
    f"{tiempo:.9f} segundos"
)


print("\n")
print("=" * 60)
print("              FIN DEL PROGRAMA")
print("=" * 60)