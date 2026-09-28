import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time


# ============================================================
#        ANÁLISIS DE GRAFO TEMPORAL Y POPULARIDAD
# ============================================================


# ============================================================
# 1. NODOS DEL GRAFO
# ============================================================

nodos = ["A", "B", "C", "D", "E"]

N = len(nodos)


# ============================================================
# 2. CONEXIONES ORIGINALES
# ============================================================
#
# Se escriben como:
#
# ("origen", "destino")
#
# Ejemplo:
# ("A", "B") significa A ---> B
#
# ============================================================

conexiones = [

    ("A", "B"),
    ("A", "D"),

    ("B", "C"),
    ("B", "D"),

    ("C", "A"),
    ("C", "D"),
    ("C", "E"),

    ("D", "A"),
    ("D", "B"),

    ("E", "D")

]


# ============================================================
# 3. FUNCIÓN PARA CREAR MATRIZ DE TRANSICIÓN
# ============================================================

def crear_matriz(conexiones):

    M = np.zeros((N, N))

    for origen in nodos:

        # Buscar destinos del nodo
        destinos = [

            destino

            for o, destino in conexiones

            if o == origen

        ]

        numero_salidas = len(destinos)

        # Repartir la probabilidad
        if numero_salidas > 0:

            for destino in destinos:

                fila = nodos.index(destino)

                columna = nodos.index(origen)

                M[fila, columna] = (
                    1 / numero_salidas
                )

    return M


# ============================================================
# 4. CREAR MATRIZ ORIGINAL
# ============================================================

M = crear_matriz(conexiones)


# ============================================================
# 5. IMPRIMIR MATRIZ ORIGINAL
# ============================================================

print("\n==============================================")
print("          MATRIZ DE TRANSICIÓN ORIGINAL")
print("==============================================")

print(M)


# ============================================================
# 6. VECTOR INICIAL T0
# ============================================================
#
# Tenemos 5 nodos.
#
# Cada nodo comienza con:
#
# 1/5 = 0.20 = 20 %
#
# ============================================================

T0 = np.ones((N, 1)) / N


print("\n==============================================")
print("                  VECTOR T0")
print("==============================================")

print(T0)


print("\nPORCENTAJES INICIALES:")

for i in range(N):

    print(
        f"{nodos[i]} = "
        f"{T0[i,0] * 100:.2f}%"
    )


# ============================================================
# 7. PEDIR NÚMERO DE ITERACIONES
# ============================================================

n = int(

    input(
        "\n¿Cuántas iteraciones deseas realizar? "
    )

)


# ============================================================
# 8. VALIDACIÓN
# ============================================================

if n <= 0:

    print(
        "\nEl número de iteraciones "
        "debe ser mayor que cero."
    )

    exit()


# ============================================================
# 9. INICIAR ANÁLISIS TEMPORAL
# ============================================================

T = T0.copy()

historial = [

    T.flatten().copy()

]


inicio = time.perf_counter()


# ============================================================
# 10. REALIZAR N ITERACIONES
# ============================================================

for iteracion in range(1, n + 1):

    # T(n) = M * T(n-1)

    T = M @ T


    # Guardar resultado

    historial.append(

        T.flatten().copy()

    )


    # Mostrar resultado

    print("\n==============================================")

    print(
        f"                  ITERACIÓN T{iteracion}"
    )

    print("==============================================")


    print("\nVECTOR:")

    print(T)


    print("\nPORCENTAJES:")


    for i in range(N):

        print(

            f"{nodos[i]} = "
            f"{T[i,0] * 100:.2f}%"

        )


# ============================================================
# 11. DETENER TIMER
# ============================================================

fin = time.perf_counter()

tiempo = fin - inicio


# ============================================================
# 12. RESULTADO FINAL
# ============================================================

print("\n==============================================")
print("             RESULTADO TEMPORAL FINAL")
print("==============================================")


for i in range(N):

    print(

        f"{nodos[i]} = "
        f"{T[i,0] * 100:.2f}%"

    )


print(

    f"\nTiempo total = "
    f"{tiempo:.9f} segundos"

)


# ============================================================
# 13. TABLA COMPLETA DE ITERACIONES
# ============================================================

historial = np.array(historial)


print("\n==============================================")
print("              TABLA DE ITERACIONES")
print("==============================================")


print(
    "\nIteración      A        B        C        D        E"
)


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
# 14. GRÁFICA DE EVOLUCIÓN TEMPORAL
# ============================================================

plt.figure(figsize=(10,6))


for i in range(N):

    plt.plot(

        range(n + 1),

        historial[:,i] * 100,

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
# 15. CREAR GRAFO ORIGINAL
# ============================================================

G = nx.DiGraph()


G.add_nodes_from(nodos)

G.add_edges_from(conexiones)


# ============================================================
# 16. POSICIONES
# ============================================================
#
# Distribución parecida a la imagen del ejercicio
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
# 17. DIBUJAR GRAFO ORIGINAL
# ============================================================

plt.figure(figsize=(11,7))


# Nodos

nx.draw_networkx_nodes(

    G,

    pos,

    node_size=2200

)


# Letras

nx.draw_networkx_labels(

    G,

    pos,

    font_size=16,

    font_weight="bold"

)


# ============================================================
# FLECHAS
# ============================================================
#
# arrows=True
#
# indica que las conexiones tienen dirección.
#
# arrowstyle="-|>"
#
# hace más visible la punta de la flecha.
#
# ============================================================

nx.draw_networkx_edges(

    G,

    pos,

    arrows=True,

    arrowstyle="-|>",

    arrowsize=30,

    width=2,

    connectionstyle="arc3,rad=0.08",

    min_source_margin=20,

    min_target_margin=20

)


plt.title(
    "Grafo temporal original\n"
    "Las flechas indican la dirección de las ligas"
)

plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
#
#        SEGUNDA PARTE DEL PROGRAMA
#
#        AUMENTAR POPULARIDAD
#
# ============================================================


print("\n\n==============================================")
print("          AUMENTAR POPULARIDAD")
print("==============================================")


nodo_popular = input(

    "\n¿Qué nodo deseas hacer más popular "
    "(A, B, C, D o E)? "

).upper()


# ============================================================
# 18. VALIDAR NODO
# ============================================================

if nodo_popular not in nodos:

    print("\nNodo no válido.")

    exit()


# ============================================================
# 19. POPULARIDAD ANTES DE MODIFICAR
# ============================================================

indice = nodos.index(
    nodo_popular
)


popularidad_antes = (
    T[indice,0] * 100
)


print(

    f"\nPopularidad actual de {nodo_popular}: "
    f"{popularidad_antes:.2f}%"

)


# ============================================================
# 20. COPIAR CONEXIONES ORIGINALES
# ============================================================

conexiones_modificadas = (
    conexiones.copy()
)


conexiones_agregadas = []


# ============================================================
# 21. AGREGAR CONEXIONES ENTRANTES
# ============================================================
#
# Para aumentar la popularidad del nodo:
#
# X ---> nodo seleccionado
#
# Solamente se agregan conexiones que
# todavía no existan.
#
# ============================================================

for origen in nodos:

    # Evitar conexión consigo mismo

    if origen != nodo_popular:

        nueva = (
            origen,
            nodo_popular
        )


        # Solamente agregar si no existe

        if nueva not in conexiones_modificadas:

            conexiones_modificadas.append(
                nueva
            )

            conexiones_agregadas.append(
                nueva
            )


# ============================================================
# 22. MOSTRAR CONEXIONES NUEVAS
# ============================================================

print("\n==============================================")
print("             CONEXIONES AGREGADAS")
print("==============================================")


if len(conexiones_agregadas) == 0:

    print(
        "\nNo fue necesario agregar conexiones."
    )

else:

    for origen, destino in conexiones_agregadas:

        print(
            f"{origen} ---> {destino}"
        )


# ============================================================
# 23. CREAR MATRIZ MODIFICADA
# ============================================================

M_nueva = crear_matriz(
    conexiones_modificadas
)


# ============================================================
# 24. IMPRIMIR MATRIZ MODIFICADA
# ============================================================

print("\n==============================================")
print("          MATRIZ DE TRANSICIÓN NUEVA")
print("==============================================")

print(M_nueva)


# ============================================================
# 25. REINICIAR EN T0
# ============================================================

T_nuevo = T0.copy()


historial_nuevo = [

    T_nuevo.flatten().copy()

]


# ============================================================
# 26. TIMER DEL NUEVO ANÁLISIS
# ============================================================

inicio2 = time.perf_counter()


# ============================================================
# 27. REALIZAR NUEVAMENTE N ITERACIONES
# ============================================================

for iteracion in range(1, n + 1):

    T_nuevo = (
        M_nueva @ T_nuevo
    )


    historial_nuevo.append(

        T_nuevo.flatten().copy()

    )


    print("\n==============================================")

    print(
        f"         NUEVA ITERACIÓN T{iteracion}"
    )

    print("==============================================")


    for i in range(N):

        print(

            f"{nodos[i]} = "
            f"{T_nuevo[i,0] * 100:.2f}%"

        )


# ============================================================
# 28. DETENER TIMER
# ============================================================

fin2 = time.perf_counter()

tiempo2 = fin2 - inicio2


# ============================================================
# 29. RESULTADO FINAL MODIFICADO
# ============================================================

print("\n==============================================")
print("         RESULTADO DESPUÉS DEL CAMBIO")
print("==============================================")


for i in range(N):

    print(

        f"{nodos[i]} = "
        f"{T_nuevo[i,0] * 100:.2f}%"

    )


popularidad_despues = (

    T_nuevo[indice,0] * 100

)


print("\n----------------------------------------------")

print(
    f"Popularidad anterior de {nodo_popular}: "
    f"{popularidad_antes:.2f}%"
)

print(
    f"Popularidad nueva de {nodo_popular}: "
    f"{popularidad_despues:.2f}%"
)

print("----------------------------------------------")


print(

    f"\nTiempo de cálculo = "
    f"{tiempo2:.9f} segundos"

)


# ============================================================
# 30. CREAR GRAFO MODIFICADO
# ============================================================

G_nuevo = nx.DiGraph()


G_nuevo.add_nodes_from(
    nodos
)


G_nuevo.add_edges_from(
    conexiones_modificadas
)


# ============================================================
# 31. DIBUJAR GRAFO MODIFICADO
# ============================================================

plt.figure(figsize=(11,7))


nx.draw_networkx_nodes(

    G_nuevo,

    pos,

    node_size=2200

)


nx.draw_networkx_labels(

    G_nuevo,

    pos,

    font_size=16,

    font_weight="bold"

)


# ============================================================
# CONEXIONES ORIGINALES EN NEGRO
# ============================================================

nx.draw_networkx_edges(

    G_nuevo,

    pos,

    edgelist=conexiones,

    arrows=True,

    arrowstyle="-|>",

    arrowsize=30,

    width=2,

    edge_color="black",

    connectionstyle="arc3,rad=0.08",

    min_source_margin=20,

    min_target_margin=20

)


# ============================================================
# CONEXIONES NUEVAS EN ROJO
# ============================================================

nx.draw_networkx_edges(

    G_nuevo,

    pos,

    edgelist=conexiones_agregadas,

    arrows=True,

    arrowstyle="-|>",

    arrowsize=35,

    width=3,

    edge_color="red",

    connectionstyle="arc3,rad=0.18",

    min_source_margin=20,

    min_target_margin=20

)


plt.title(

    f"Grafo modificado\n"
    f"Aumento de popularidad del nodo {nodo_popular}"

)

plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
# 32. COMPARACIÓN ANTES Y DESPUÉS
# ============================================================

historial_nuevo = np.array(
    historial_nuevo
)


plt.figure(figsize=(10,6))


# Antes

plt.plot(

    range(n + 1),

    historial[:,indice] * 100,

    marker="o",

    label="Antes"

)


# Después

plt.plot(

    range(n + 1),

    historial_nuevo[:,indice] * 100,

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

    f"Popularidad del nodo {nodo_popular}\n"
    "Antes y después de modificar el grafo"

)

plt.xticks(
    range(n + 1)
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.show()