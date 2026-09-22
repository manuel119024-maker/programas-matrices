import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time

# -------------------------------------------------
# MATRIZ ORIGINAL
# -------------------------------------------------

A = np.array([
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0]
])

# -------------------------------------------------
# CALCULAR POPULARIDAD ORIGINAL
# -------------------------------------------------

A2 = A @ A
popularidad = np.diag(A2)

print("MATRIZ ORIGINAL:")
print(A)

print("\nPOPULARIDAD ORIGINAL:")

for i in range(len(A)):
    print(f"Nodo {i+1}: {popularidad[i]} conexiones")

# Popularidad máxima de la red original
popularidad_maxima = np.max(popularidad)

print("\nPopularidad máxima original:",
      popularidad_maxima)

# -------------------------------------------------
# SELECCIONAR NODO
# -------------------------------------------------

nodo = int(
    input("\n¿Qué nodo deseas hacer más popular? ")
)

if nodo < 1 or nodo > len(A):

    print("Nodo no válido.")

else:

    indice = nodo - 1

    # Copiar la matriz original
    A_nueva = A.copy()

    popularidad_actual = popularidad[indice]

    # -------------------------------------------------
    # ENERGÍA MÍNIMA
    # -------------------------------------------------

    energia_necesaria = (
        popularidad_maxima - popularidad_actual
    )

    print(
        f"\nPopularidad actual del nodo {nodo}: "
        f"{popularidad_actual}"
    )

    print(
        f"Popularidad objetivo: "
        f"{popularidad_maxima}"
    )

    print(
        f"Energía mínima necesaria: "
        f"{energia_necesaria}"
    )

    # -------------------------------------------------
    # INICIAR TIMER
    # -------------------------------------------------

    inicio = time.perf_counter()

    conexiones_nuevas = []

    # -------------------------------------------------
    # AGREGAR CONEXIONES
    # -------------------------------------------------

    for i in range(len(A)):

        # Evitar conectarse consigo mismo
        if i != indice:

            # Solamente agregar si no existe
            if A_nueva[indice, i] == 0:

                # Crear conexión bidireccional
                A_nueva[indice, i] = 1
                A_nueva[i, indice] = 1

                conexiones_nuevas.append(
                    (indice, i)
                )

                if (
                    len(conexiones_nuevas)
                    == energia_necesaria
                ):
                    break

    # -------------------------------------------------
    # NUEVA POPULARIDAD
    # -------------------------------------------------

    A2_nueva = A_nueva @ A_nueva

    popularidad_nueva = np.diag(A2_nueva)

    # -------------------------------------------------
    # DETENER TIMER
    # -------------------------------------------------

    fin = time.perf_counter()

    tiempo = fin - inicio

    # -------------------------------------------------
    # RESULTADOS
    # -------------------------------------------------

    print("\n--------------------------------")
    print("RESULTADOS")
    print("--------------------------------")

    print("\nConexiones nuevas:")

    if conexiones_nuevas:

        for a, b in conexiones_nuevas:

            print(
                f"Nodo {a+1} <--> Nodo {b+1}"
            )

    else:

        print(
            "No se necesitan conexiones nuevas."
        )

    print("\nMATRIZ MODIFICADA:")
    print(A_nueva)

    print("\nNUEVA POPULARIDAD:")

    for i in range(len(A)):

        print(
            f"Nodo {i+1}: "
            f"{popularidad_nueva[i]} conexiones"
        )

    print(
        f"\nPopularidad final del nodo {nodo}: "
        f"{popularidad_nueva[indice]}"
    )

    print(
        f"Energía utilizada: "
        f"{len(conexiones_nuevas)}"
    )

    print(
        f"Tiempo de cálculo: "
        f"{tiempo:.9f} segundos"
    )

    # =================================================
    # CREAR GRAFO
    # =================================================

    G_original = nx.from_numpy_array(A)

    G_nuevo = nx.from_numpy_array(A_nueva)

    # Etiquetas 1 - 6
    etiquetas = {
        i: i + 1
        for i in range(len(A))
    }

    # -------------------------------------------------
    # POSICIÓN DE LOS NODOS
    # -------------------------------------------------

    pos = nx.spring_layout(
        G_nuevo,
        seed=10
    )

    # =================================================
    # GRÁFICA ORIGINAL
    # =================================================

    plt.figure(figsize=(7, 6))

    nx.draw_networkx_nodes(
        G_original,
        pos,
        node_size=1500
    )

    nx.draw_networkx_edges(
        G_original,
        pos,
        width=2,
        edge_color="black"
    )

    nx.draw_networkx_labels(
        G_original,
        pos,
        labels=etiquetas,
        font_size=14
    )

    plt.title("Red original")

    plt.axis("off")

    plt.show()

    # =================================================
    # GRÁFICA FINAL
    # =================================================

    plt.figure(figsize=(7, 6))

    # -------------------------------------------------
    # DIBUJAR NODOS
    # -------------------------------------------------

    nx.draw_networkx_nodes(
        G_nuevo,
        pos,
        node_size=1500
    )

    # -------------------------------------------------
    # CONEXIONES ORIGINALES
    # Se conservan en NEGRO
    # -------------------------------------------------

    conexiones_originales = list(
        G_original.edges()
    )

    nx.draw_networkx_edges(
        G_nuevo,
        pos,
        edgelist=conexiones_originales,
        edge_color="black",
        width=2
    )

    # -------------------------------------------------
    # CONEXIONES NUEVAS
    # Se muestran en ROJO
    # -------------------------------------------------

    nx.draw_networkx_edges(
        G_nuevo,
        pos,
        edgelist=conexiones_nuevas,
        edge_color="red",
        width=4
    )

    # -------------------------------------------------
    # NÚMEROS DE LOS NODOS
    # -------------------------------------------------

    nx.draw_networkx_labels(
        G_nuevo,
        pos,
        labels=etiquetas,
        font_size=14
    )

    plt.title(
        f"Red modificada - Nodo {nodo}"
    )

    plt.axis("off")

    plt.show()