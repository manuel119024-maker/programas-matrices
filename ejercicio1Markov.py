import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time

# ============================================================
#       ANÁLISIS DE GRAFO TEMPORAL + POPULARIDAD
# ============================================================

# ============================================================
# 1. NODOS
# ============================================================

nodos = ["A", "B", "C", "D", "E"]

N = len(nodos)


# ============================================================
# 2. DEFINIR CONEXIONES DEL GRAFO
# ============================================================
#
# Las conexiones se escriben:
#
# origen -> destino
#
# De acuerdo con la gráfica:
#
# A -> B
# B -> C
# C -> A
# C -> D
# C -> E
# D -> A
# D -> B
# B -> D
# E -> C
#
# ============================================================

conexiones = [
    ("A", "B"),
    ("B", "C"),
    ("C", "A"),
    ("C", "D"),
    ("C", "E"),
    ("D", "A"),
    ("D", "B"),
    ("B", "D"),
    ("E", "C")
]


# ============================================================
# 3. CREAR MATRIZ DE TRANSICIÓN
# ============================================================
#
# Cada nodo reparte su porcentaje entre todas
# sus conexiones de salida.
#
# Ejemplo:
#
# Si C tiene 3 salidas:
#
# C -> A
# C -> D
# C -> E
#
# Cada una recibe:
#
# 1/3
#
# ============================================================

M = np.zeros((N, N))


for origen in nodos:

    # Buscar conexiones que salen del nodo
    destinos = [
        destino
        for o, destino in conexiones
        if o == origen
    ]

    numero_salidas = len(destinos)

    if numero_salidas > 0:

        for destino in destinos:

            i = nodos.index(destino)
            j = nodos.index(origen)

            M[i, j] = 1 / numero_salidas


# ============================================================
# 4. MOSTRAR MATRIZ
# ============================================================

print("\n==========================================")
print("       MATRIZ DE TRANSICIÓN ORIGINAL")
print("==========================================")

print(M)


# ============================================================
# 5. VECTOR INICIAL
# ============================================================
#
# Como tenemos 5 nodos:
#
# 1 / 5 = 0.20 = 20 %
#
# ============================================================

T = np.ones((N, 1)) / N


print("\n==========================================")
print("              VECTOR T0")
print("==========================================")

print(T)


print("\nPORCENTAJES INICIALES:")

for i in range(N):

    print(
        f"{nodos[i]} = "
        f"{T[i, 0] * 100:.2f}%"
    )


# ============================================================
# 6. PEDIR NÚMERO DE ITERACIONES
# ============================================================

n = int(
    input("\n¿Cuántas iteraciones deseas realizar? ")
)


# ============================================================
# 7. GUARDAR HISTORIAL
# ============================================================

historial = []

historial.append(
    T.flatten().copy()
)


# ============================================================
# 8. INICIAR TIMER
# ============================================================

inicio = time.perf_counter()


# ============================================================
# 9. REALIZAR N ITERACIONES
# ============================================================

for iteracion in range(1, n + 1):

    # T(n) = M * T(n-1)

    T = M @ T

    historial.append(
        T.flatten().copy()
    )

    print("\n==========================================")
    print(f"                ITERACIÓN T{iteracion}")
    print("==========================================")

    print("\nVector:")

    print(T)

    print("\nPorcentajes:")

    for i in range(N):

        print(
            f"{nodos[i]} = "
            f"{T[i, 0] * 100:.2f}%"
        )


# ============================================================
# 10. DETENER TIMER
# ============================================================

fin = time.perf_counter()

tiempo = fin - inicio


# ============================================================
# 11. RESULTADO FINAL
# ============================================================

print("\n==========================================")
print("          RESULTADO TEMPORAL FINAL")
print("==========================================")

for i in range(N):

    print(
        f"{nodos[i]} = "
        f"{T[i, 0] * 100:.2f}%"
    )


print(
    f"\nTiempo de cálculo: "
    f"{tiempo:.9f} segundos"
)


# ============================================================
# 12. TABLA DE ITERACIONES
# ============================================================

historial = np.array(historial)


print("\n==========================================")
print("          TABLA DE ITERACIONES")
print("==========================================")

print("\nIteración      A       B       C       D       E")


for t in range(n + 1):

    print(
        f"T{t:<8}"
        f"{historial[t,0]*100:8.2f}% "
        f"{historial[t,1]*100:8.2f}% "
        f"{historial[t,2]*100:8.2f}% "
        f"{historial[t,3]*100:8.2f}% "
        f"{historial[t,4]*100:8.2f}%"
    )


# ============================================================
# 13. GRÁFICA DE EVOLUCIÓN TEMPORAL
# ============================================================

plt.figure(figsize=(10, 6))


for i in range(N):

    plt.plot(
        range(n + 1),
        historial[:, i] * 100,
        marker="o",
        label=nodos[i]
    )


plt.xlabel("Iteración")

plt.ylabel("Porcentaje (%)")

plt.title(
    "Evolución temporal de los nodos"
)

plt.xticks(
    range(n + 1)
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.show()


# ============================================================
# 14. CREAR GRAFO ORIGINAL DIRIGIDO
# ============================================================

G = nx.DiGraph()

G.add_nodes_from(nodos)

G.add_edges_from(conexiones)


# ============================================================
# 15. POSICIÓN DE LOS NODOS
# ============================================================
#
# Parecida a la gráfica de clase
#
# ============================================================

pos = {

    "A": (0, 2),

    "B": (3, 2),

    "C": (3, 0),

    "D": (0, 0),

    "E": (5, 0)

}


# ============================================================
# 16. GRAFICAR RED ORIGINAL
# ============================================================

plt.figure(figsize=(10, 6))


nx.draw_networkx_nodes(
    G,
    pos,
    node_size=2000
)


nx.draw_networkx_labels(
    G,
    pos,
    font_size=15,
    font_weight="bold"
)


# IMPORTANTE:
# arrows=True muestra la dirección de las conexiones

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=30,
    width=2,
    connectionstyle="arc3,rad=0.08"
)


plt.title(
    "Grafo temporal original - Dirección de las conexiones"
)

plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
#     SEGUNDA PARTE
#     AUMENTAR POPULARIDAD DE UN NODO
# ============================================================


print("\n==========================================")
print("       AUMENTAR POPULARIDAD DE UN NODO")
print("==========================================")


nodo_popular = input(
    "\n¿Qué nodo deseas hacer más popular "
    "(A, B, C, D o E)? "
).upper()


# ============================================================
# 17. VALIDAR NODO
# ============================================================

if nodo_popular not in nodos:

    print("\nNodo no válido.")

else:

    # ========================================================
    # 18. MOSTRAR POPULARIDAD ACTUAL
    # ========================================================

    indice_popular = nodos.index(
        nodo_popular
    )

    print(
        f"\nPopularidad actual de {nodo_popular}: "
        f"{T[indice_popular,0] * 100:.2f}%"
    )


    # ========================================================
    # 19. COPIAR CONEXIONES
    # ========================================================

    conexiones_nuevas = conexiones.copy()

    agregadas = []


    # ========================================================
    # 20. BUSCAR NODOS SIN CONEXIÓN HACIA EL NODO ELEGIDO
    # ========================================================
    #
    # Para aumentar la popularidad del nodo seleccionado
    # agregamos conexiones ENTRANTES.
    #
    # Ejemplo:
    #
    # Si queremos hacer más popular a C:
    #
    # X -> C
    #
    # ========================================================

    for origen in nodos:

        if origen != nodo_popular:

            conexion = (
                origen,
                nodo_popular
            )

            if conexion not in conexiones_nuevas:

                conexiones_nuevas.append(
                    conexion
                )

                agregadas.append(
                    conexion
                )


    # ========================================================
    # 21. MOSTRAR NUEVAS CONEXIONES
    # ========================================================

    print("\nCONEXIONES AGREGADAS:")


    if len(agregadas) == 0:

        print(
            "El nodo ya recibe conexiones "
            "de todos los demás nodos."
        )

    else:

        for origen, destino in agregadas:

            print(
                f"{origen} -> {destino}"
            )


    # ========================================================
    # 22. CREAR NUEVA MATRIZ DE TRANSICIÓN
    # ========================================================

    M_nueva = np.zeros((N, N))


    for origen in nodos:

        destinos = [

            destino

            for o, destino in conexiones_nuevas

            if o == origen

        ]

        numero_salidas = len(destinos)


        if numero_salidas > 0:

            for destino in destinos:

                i = nodos.index(destino)

                j = nodos.index(origen)

                M_nueva[i, j] = (
                    1 / numero_salidas
                )


    # ========================================================
    # 23. IMPRIMIR NUEVA MATRIZ
    # ========================================================

    print("\n==========================================")
    print("        NUEVA MATRIZ DE TRANSICIÓN")
    print("==========================================")

    print(M_nueva)


    # ========================================================
    # 24. NUEVO VECTOR INICIAL
    # ========================================================

    T_nuevo = np.ones(
        (N, 1)
    ) / N


    historial_nuevo = [

        T_nuevo.flatten().copy()

    ]


    # ========================================================
    # 25. TIMER DEL NUEVO ANÁLISIS
    # ========================================================

    inicio2 = time.perf_counter()


    # ========================================================
    # 26. REPETIR LAS MISMAS N ITERACIONES
    # ========================================================

    for iteracion in range(1, n + 1):

        T_nuevo = (
            M_nueva @ T_nuevo
        )

        historial_nuevo.append(
            T_nuevo.flatten().copy()
        )


    fin2 = time.perf_counter()

    tiempo2 = fin2 - inicio2


    # ========================================================
    # 27. RESULTADO DESPUÉS DE MODIFICAR EL GRAFO
    # ========================================================

    print("\n==========================================")
    print("       NUEVO RESULTADO TEMPORAL")
    print("==========================================")


    for i in range(N):

        print(
            f"{nodos[i]} = "
            f"{T_nuevo[i,0] * 100:.2f}%"
        )


    print(
        f"\nNueva popularidad de {nodo_popular}: "
        f"{T_nuevo[indice_popular,0] * 100:.2f}%"
    )


    print(
        f"\nTiempo de cálculo: "
        f"{tiempo2:.9f} segundos"
    )


    # ========================================================
    # 28. CREAR GRAFO MODIFICADO
    # ========================================================

    G_nuevo = nx.DiGraph()

    G_nuevo.add_nodes_from(
        nodos
    )

    G_nuevo.add_edges_from(
        conexiones_nuevas
    )


    # ========================================================
    # 29. GRAFICAR RED MODIFICADA
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )


    nx.draw_networkx_nodes(
        G_nuevo,
        pos,
        node_size=2000
    )


    nx.draw_networkx_labels(
        G_nuevo,
        pos,
        font_size=15,
        font_weight="bold"
    )


    # --------------------------------------------------------
    # CONEXIONES ORIGINALES
    # --------------------------------------------------------

    nx.draw_networkx_edges(
        G_nuevo,
        pos,
        edgelist=conexiones,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=30,
        width=2,
        edge_color="black",
        connectionstyle="arc3,rad=0.08"
    )


    # --------------------------------------------------------
    # CONEXIONES NUEVAS EN ROJO
    # --------------------------------------------------------

    nx.draw_networkx_edges(
        G_nuevo,
        pos,
        edgelist=agregadas,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=30,
        width=3,
        edge_color="red",
        connectionstyle="arc3,rad=0.15"
    )


    plt.title(
        f"Grafo modificado - Mayor popularidad de {nodo_popular}"
    )

    plt.axis("off")

    plt.tight_layout()

    plt.show()


    # ========================================================
    # 30. COMPARAR EVOLUCIÓN DEL NODO SELECCIONADO
    # ========================================================

    historial_nuevo = np.array(
        historial_nuevo
    )


    plt.figure(
        figsize=(10, 6)
    )


    plt.plot(
        range(n + 1),
        historial[:, indice_popular] * 100,
        marker="o",
        label="Antes"
    )


    plt.plot(
        range(n + 1),
        historial_nuevo[:, indice_popular] * 100,
        marker="o",
        label="Después"
    )


    plt.xlabel(
        "Iteración"
    )

    plt.ylabel(
        "Porcentaje (%)"
    )

    plt.title(
        f"Comparación de popularidad del nodo {nodo_popular}"
    )

    plt.xticks(
        range(n + 1)
    )

    plt.legend()

    plt.grid()

    plt.tight_layout()

    plt.show()