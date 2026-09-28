# ============================================================
# GRAFO TEMPORAL - N ITERACIONES
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time


# ============================================================
# 1. MATRIZ DE ADYACENCIA
# ============================================================

M = np.array([
    [0,   0,   1/2, 1/2],
    [1,   0,   0,   1/2],
    [0,   1/2, 0,   0],
    [0,   1/2, 1/2, 0]
], dtype=float)


# ============================================================
# 2. NOMBRES DE LOS NODOS
# ============================================================

nodos = ["A", "B", "C", "D"]


# ============================================================
# 3. VECTOR INICIAL T0
# Cada nodo inicia con 25%
# ============================================================

T = np.array([
    [1/4],
    [1/4],
    [1/4],
    [1/4]
], dtype=float)


# ============================================================
# 4. MOSTRAR MATRIZ ORIGINAL
# ============================================================

print("\n========================================")
print("      MATRIZ DE ADYACENCIA ORIGINAL")
print("========================================")

print(M)


# ============================================================
# 5. MOSTRAR VECTOR INICIAL T0
# ============================================================

print("\n========================================")
print("              VECTOR T0")
print("========================================")

print(T)


print("\nPORCENTAJES INICIALES:")

for i in range(len(nodos)):

    print(
        f"Nodo {nodos[i]} = "
        f"{T[i, 0] * 100:.2f}%"
    )


# ============================================================
# 6. PEDIR NÚMERO DE ITERACIONES
# ============================================================

n = int(
    input("\n¿Cuántas iteraciones deseas realizar? ")
)


# ============================================================
# 7. VALIDAR NÚMERO DE ITERACIONES
# ============================================================

if n < 1:

    print(
        "\nERROR: El número de iteraciones "
        "debe ser mayor que cero."
    )

else:

    # ========================================================
    # 8. CREAR HISTORIAL
    # ========================================================

    historial = []

    # Guardamos T0
    historial.append(
        T.flatten().copy()
    )


    # ========================================================
    # 9. INICIAR TIMER
    # ========================================================

    inicio = time.perf_counter()


    # ========================================================
    # 10. REALIZAR N ITERACIONES
    # ========================================================

    for iteracion in range(1, n + 1):

        # ----------------------------------------------------
        # Multiplicación matricial
        #
        # T(n) = M * T(n-1)
        # ----------------------------------------------------

        T = M @ T


        # ----------------------------------------------------
        # Guardar resultado
        # ----------------------------------------------------

        historial.append(
            T.flatten().copy()
        )


        # ----------------------------------------------------
        # Mostrar número de iteración
        # ----------------------------------------------------

        print("\n========================================")
        print(f"              ITERACIÓN T{iteracion}")
        print("========================================")


        # ----------------------------------------------------
        # Mostrar vector
        # ----------------------------------------------------

        print("\nVECTOR RESULTADO:")

        print(T)


        # ----------------------------------------------------
        # Mostrar porcentajes
        # ----------------------------------------------------

        print("\nPORCENTAJES:")

        for i in range(len(nodos)):

            print(
                f"Nodo {nodos[i]} = "
                f"{T[i, 0]:.6f} = "
                f"{T[i, 0] * 100:.2f}%"
            )


        # ----------------------------------------------------
        # Mostrar suma de porcentajes
        # ----------------------------------------------------

        suma_iteracion = np.sum(T)

        print(
            f"\nSuma total T{iteracion} = "
            f"{suma_iteracion * 100:.2f}%"
        )


    # ========================================================
    # 11. DETENER TIMER
    # ========================================================

    fin = time.perf_counter()

    tiempo = fin - inicio


    # ========================================================
    # 12. RESULTADO FINAL
    # ========================================================

    print("\n========================================")
    print("             RESULTADO FINAL")
    print("========================================")

    print(
        f"\nNúmero de iteraciones realizadas: {n}"
    )


    # ========================================================
    # 13. VECTOR FINAL
    # ========================================================

    print(f"\nVECTOR FINAL T{n}:")

    print(T)


    # ========================================================
    # 14. PORCENTAJES FINALES
    # ========================================================

    print("\nPORCENTAJES FINALES:")

    for i in range(len(nodos)):

        print(
            f"Nodo {nodos[i]} = "
            f"{T[i, 0] * 100:.2f}%"
        )


    # ========================================================
    # 15. SUMA FINAL
    # ========================================================

    suma_final = np.sum(T)

    print(
        f"\nSuma total = "
        f"{suma_final * 100:.2f}%"
    )


    # ========================================================
    # 16. MOSTRAR TIMER
    # ========================================================

    print(
        f"\nTiempo total de cálculo = "
        f"{tiempo:.9f} segundos"
    )


    # ========================================================
    # 17. MOSTRAR TODAS LAS ITERACIONES EN TABLA
    # ========================================================

    historial = np.array(historial)

    print("\n========================================")
    print("       TABLA DE TODAS LAS ITERACIONES")
    print("========================================")

    print("\nIteración       A        B        C        D")

    for t in range(n + 1):

        print(
            f"T{t:<10}"
            f"{historial[t,0]*100:8.2f}% "
            f"{historial[t,1]*100:8.2f}% "
            f"{historial[t,2]*100:8.2f}% "
            f"{historial[t,3]*100:8.2f}%"
        )


    # ========================================================
    # 18. CREAR GRÁFICA DE EVOLUCIÓN
    # ========================================================

    plt.figure(figsize=(10, 6))

    for i in range(len(nodos)):

        plt.plot(
            range(n + 1),
            historial[:, i] * 100,
            marker="o",
            label=f"Nodo {nodos[i]}"
        )


    # ========================================================
    # 19. CONFIGURACIÓN DE LA GRÁFICA
    # ========================================================

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


    # ========================================================
    # 20. MOSTRAR GRÁFICA
    # ========================================================

    plt.show()


    # ========================================================
    # 21. CREAR GRAFO DIRIGIDO
    # ========================================================

    G = nx.DiGraph()

    # Agregar nodos
    for nodo in nodos:

        G.add_node(nodo)


    # ========================================================
    # 22. AGREGAR CONEXIONES DEL GRAFO
    # ========================================================

    for i in range(len(M)):

        for j in range(len(M)):

            if M[i, j] != 0:

                G.add_edge(
                    nodos[i],
                    nodos[j],
                    weight=M[i, j]
                )


    # ========================================================
    # 23. POSICIONES DE LOS NODOS
    # Parecidas a la imagen del ejercicio
    # ========================================================

    pos = {

        "A": (0, 1),

        "B": (2, 1),

        "C": (2, 0),

        "D": (0, 0)

    }


    # ========================================================
    # 24. GRAFICAR GRAFO
    # ========================================================

    plt.figure(figsize=(8, 6))


    # Dibujar nodos
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2000
    )


    # Dibujar nombres
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=14
    )


    # Dibujar conexiones dirigidas
    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True,
        arrowsize=25,
        width=2,
        connectionstyle="arc3,rad=0.08"
    )


    # ========================================================
    # 25. MOSTRAR VALORES DE LAS CONEXIONES
    # ========================================================

    pesos = nx.get_edge_attributes(
        G,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=pesos
    )


    # ========================================================
    # 26. CONFIGURACIÓN DEL GRAFO
    # ========================================================

    plt.title(
        "Grafo temporal - Matriz de adyacencia"
    )

    plt.axis("off")

    plt.tight_layout()


    # ========================================================
    # 27. MOSTRAR GRAFO
    # ========================================================

    plt.show()